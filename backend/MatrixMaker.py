from datetime import datetime
from urllib.parse import urlparse, parse_qs

import numpy as np
import networkx as nx
import psycopg2
from os import environ
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import json

# Import Gemini functionality
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
from typing import TypedDict, List, Dict
from time import perf_counter

load_dotenv()

conn = psycopg2.connect(environ.get("PYTHON_DATABASE_URL"))
cur = conn.cursor()

# Configure Gemini
try:
    api_key = environ.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        GEMINI_ENABLED = True
    else:
        print("Warning: GEMINI_API_KEY not found. Using rule-based compatibility only.")
        GEMINI_ENABLED = False
except Exception as e:
    print(f"Warning: Could not configure Gemini: {e}. Using rule-based compatibility only.")
    GEMINI_ENABLED = False

# --- Type Definitions ---
class RoommateProfile(TypedDict):
    """Represents the details for a single roommate."""
    id: str
    self_description: str
    ideal_roommate: str

CompatibilityMatrix = Dict[str, Dict[str, float]]

# --- Original MatrixMaker Functions ---

def overnightGuest(answer1, answer2):
    answer1, answer2 = {"yes": 1, 'rather-no': 0.5, 'no': 0}[answer1], {"yes": 1, 'rather-no': 0.5, 'no': 0}[answer2]

    if answer1 == answer2:
        return 1
    elif abs(answer1 - answer2) == 1:
        return 0.5
    else:
        return 0

def textSimilarity(answer1, answer2):
    SetAnswer1 = set([x.lower() for x in answer1])
    SetAnswer2 = set([x.lower() for x in answer2])
    rating = max(len(SetAnswer1 & SetAnswer2), 1) / max(len(SetAnswer1 | SetAnswer2), 1)
    return rating

def personalityType(answer1, answer2):
    if answer1 == answer2:
        return 1
    else:
        return 0

def tidiness(tidy1, tidy2, care1, care2):
    tidy1 = tidy1 / 5
    tidy2 = tidy2 / 5
    care1 = care1 / 5
    care2 = care2 / 5

    mutualTidiness = 1 - abs(tidy1 - tidy2)
    agreeable1 = 1 - abs(tidy1 - care2)
    agreeable2 = 1 - abs(tidy2 - care1)

    compatibility = (agreeable1 + agreeable2 + mutualTidiness) / 3
    return round(compatibility, 2)

def minutes(time):
    return time * 30

def timeSimilarity(time1, time2):
    difference = abs(minutes(time1) - minutes(time2))
    difference = min(difference, 1440 - difference)
    difference = 1 - difference / 480
    if difference < 0:
        return 0
    else:
        return difference

def weekdayTimings(sleep1, wake1, sleep2, wake2):
    sleep = timeSimilarity(sleep1, sleep2)
    wake = timeSimilarity(wake1, wake2)
    return round((sleep + wake) / 2, 2)

def workTimings(earliest1, latest1, earliest2, latest2):
    start = timeSimilarity(earliest1, earliest2)
    end = timeSimilarity(latest1, latest2)
    return round((start - end) / 2, 2)

def nightOutTimings(sleep1, sleep2):
    return timeSimilarity(sleep1, sleep2)

def overallTimings(weekdayScore, workScore, nightOutScore):
    return round((weekdayScore + workScore + nightOutScore) / 2, 2)

def timingCompatibility(sleep1, sleep2, wake1, wake2, earliestwork1, earliestwork2,
                        latestwork1, latestwork2, nightOutsleep1, nightOutsleep2):
    weekdayScore = weekdayTimings(sleep1, wake1, sleep2, wake2)
    workScore = workTimings(earliestwork1, latestwork1, earliestwork2, latestwork2)
    nightOutScore = nightOutTimings(nightOutsleep1, nightOutsleep2)
    result = overallTimings(weekdayScore, workScore, nightOutScore)
    return result

def finalCompatibility(person1, person2):
    """Calculate rule-based compatibility score (0-7 scale)"""
    curr = conn.cursor(cursor_factory=RealDictCursor)
    curr.execute('SELECT * FROM "Answers" WHERE "studentId" = %s;', (person1,))
    all1 = curr.fetchone()

    curr.execute('SELECT * FROM "Answers" WHERE "studentId" = %s;', (person2,))
    all2 = curr.fetchone()

    guest = overnightGuest(all1["overnightGuests"], all2["overnightGuests"])
    musicG = textSimilarity(all1["musicArtists"], all2["musicArtists"])
    musicA = textSimilarity(all1["musicGenres"], all2["musicGenres"])
    sport = textSimilarity(all1["sportsWatched"], all2["sportsWatched"])
    personality = personalityType(all1["introvertExtrovert"], all2["introvertExtrovert"])
    cleanliness = tidiness(all1["tidiness"], all2["tidiness"],
                           all1["careAboutTidiness"], all2["careAboutTidiness"])

    times = timingCompatibility(
        all1["normalWeekdayBedtime"], all2["normalWeekdayBedtime"],
        all1["normalWeekdayStartTime"], all2["normalWeekdayStartTime"],
        all1["workStartTime"], all2["workStartTime"],
        all1["workEndTime"], all2["workEndTime"],
        all1["nightOutBedtime"], all2["nightOutBedtime"]
    )

    compatibility = guest + musicG + musicA + sport + personality + cleanliness + times
    return compatibility

# --- Gemini Integration Functions ---

def get_gemini_compatibility_matrix(roommates: List[RoommateProfile]) -> CompatibilityMatrix:
    """
    Get AI-based compatibility scores from Gemini.
    Returns scores normalized to 0-1 scale.
    """
    if not GEMINI_ENABLED or len(roommates) < 2:
        return {}

    compatibility_tool = Tool(
        function_declarations=[
            FunctionDeclaration(
                name="RecordCompatibilityScores",
                description="Records the compatibility scores for all unique pairs of roommates.",
                parameters={
                    "type": "OBJECT",
                    "properties": {
                        "compatibilities": {
                            "type": "ARRAY",
                            "description": "A list of compatibility scores for each unique pair of roommates.",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "roommate1_id": {
                                        "type": "STRING",
                                        "description": "The unique ID of the first roommate in the pair."
                                    },
                                    "roommate2_id": {
                                        "type": "STRING",
                                        "description": "The unique ID of the second roommate in the pair."
                                    },
                                    "score": {
                                        "type": "NUMBER",
                                        "description": "The compatibility score from 0.0 (incompatible) to 1.0 (perfectly compatible)."
                                    }
                                },
                                "required": ["roommate1_id", "roommate2_id", "score"]
                            }
                        }
                    },
                    "required": ["compatibilities"]
                },
            )
        ]
    )

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash-lite",
        generation_config={"temperature": 0.0},
        tools=[compatibility_tool],
        tool_config={"function_calling_config": "ANY"}
    )

    # Build prompt
    prompt_parts = [
        "You are a highly logical and consistent roommate compatibility calculator.",
        "Your task is to analyze the self-descriptions and ideal roommate descriptions of a group of individuals.",
        "For EVERY unique pair of individuals, you must produce a single, numeric compatibility score between 0.0 and 1.0.",
        "Base your score on a holistic analysis of how well each person's self-description matches the other's ideal, and their general lifestyle compatibility.",
        "Analyze the following roommate profiles carefully:\n"
    ]

    for r in roommates:
        prompt_parts.append(f"--- Roommate ID: {r['id']} ---")
        prompt_parts.append(f"Self-description: \"{r['self_description']}\"")
        prompt_parts.append(f"Ideal roommate: \"{r['ideal_roommate']}\"\n")

    prompt_parts.append("Now, provide the compatibility score for every unique pair.")
    prompt = "\n".join(prompt_parts)

    try:
        start_time = perf_counter()
        response = model.generate_content(prompt)
        end_time = perf_counter()
        print(f"Gemini API call took {end_time - start_time:.2f} seconds for {len(roommates)} roommates")

        function_call = response.candidates[0].content.parts[0].function_call
        if function_call.name != "RecordCompatibilityScores":
            raise ValueError(f"Unexpected function call: {function_call.name}")

        compatibility_list = function_call.args['compatibilities']

        # Build matrix
        all_ids = [r['id'] for r in roommates]
        matrix: CompatibilityMatrix = {uid: {} for uid in all_ids}

        # Initialize with self-compatibility
        for uid in all_ids:
            matrix[uid][uid] = 1.0

        # Populate from AI response
        for pair in compatibility_list:
            id1 = pair['roommate1_id']
            id2 = pair['roommate2_id']
            score = max(0.0, min(1.0, float(pair['score'])))

            if id1 in matrix and id2 in matrix:
                matrix[id1][id2] = score
                matrix[id2][id1] = score
            else:
                print(f"Warning: Invalid ID pair from Gemini: ({id1}, {id2})")

        return matrix

    except Exception as e:
        print(f"Error getting Gemini compatibility: {e}")
        return {}

def fetch_roommate_profiles(ids: List[str]) -> List[RoommateProfile]:
    """Fetch self-descriptions and ideal roommate descriptions from database."""
    curr = conn.cursor(cursor_factory=RealDictCursor)
    profiles = []

    for student_id in ids:
        curr.execute('''
                     SELECT "studentId", "selfDescription", "idealRoommate"
                     FROM "Answers"
                     WHERE "studentId" = %s;
                     ''', (student_id,))

        result = curr.fetchone()
        if result and result.get("selfDescription") and result.get("idealRoommate"):
            profiles.append({
                "id": student_id,
                "self_description": result["selfDescription"],
                "ideal_roommate": result["idealRoommate"]
            })

    return profiles

# --- Enhanced Matrix Population ---

def populateMatrix(ids, use_gemini=True, gemini_weight=0.5):
    """
    Populate compatibility matrix using both rule-based and AI-based scoring.

    Args:
        ids: List of student IDs
        use_gemini: Whether to include Gemini AI scoring
        gemini_weight: Weight for Gemini score (0-1). Rule-based gets (1-gemini_weight)

    Returns:
        Combined compatibility matrix
    """
    # Get size of matrix
    matrix = [[0 for i in range(len(ids))] for j in range(len(ids))]

    # Fetch gender information
    curr = conn.cursor(cursor_factory=RealDictCursor)
    curr.execute('SELECT "studentId","gender" FROM "Answers"')
    genders = curr.fetchall()

    genderDict = {}
    for item in genders:
        genderDict[item["studentId"]] = item["gender"]

    # Get Gemini compatibility scores if enabled
    gemini_matrix = {}
    if use_gemini and GEMINI_ENABLED:
        print("Fetching profiles for Gemini analysis...")
        profiles = fetch_roommate_profiles(ids)

        if len(profiles) >= 2:
            print(f"Calculating AI compatibility for {len(profiles)} profiles...")
            gemini_matrix = get_gemini_compatibility_matrix(profiles)
        else:
            print(f"Warning: Only {len(profiles)} profiles have descriptions. Need at least 2 for Gemini.")

    # Calculate combined compatibility
    for i in range(len(ids)):
        for j in range(i, len(ids)):
            person1 = ids[i]
            person2 = ids[j]

            genderi = genderDict.get(person1)
            genderj = genderDict.get(person2)

            if i == j:
                matrix[i][j] = 0
            elif genderi != genderj:
                matrix[i][j] = 0
            else:
                # Calculate rule-based compatibility (0-7 scale)
                rule_comp = finalCompatibility(person1, person2)
                # Normalize to 0-1 scale
                rule_comp_normalized = rule_comp / 7.0

                # Get Gemini score if available
                gemini_comp = 0.0
                if person1 in gemini_matrix and person2 in gemini_matrix.get(person1, {}):
                    gemini_comp = gemini_matrix[person1][person2]

                # Combine scores
                if gemini_comp > 0:
                    combined_comp = (rule_comp_normalized * (1 - gemini_weight) +
                                     gemini_comp * gemini_weight)
                    # Scale back to original range for consistency
                    final_comp = combined_comp * 7.0
                    print(f"{person1}-{person2}: Rule={rule_comp:.2f}, Gemini={gemini_comp:.2f}, Combined={final_comp:.2f}")
                else:
                    final_comp = rule_comp
                    print(f"{person1}-{person2}: Rule-only={final_comp:.2f}")

                matrix[i][j] = final_comp
                matrix[j][i] = final_comp

    return matrix

# --- Rest of Original Functions ---

def averageMatrix(tab):
    mat = [["" for y in range(len(tab))] for x in range(len(tab))]
    for i in range(len(tab)):
        for j in range(i, len(tab)):
            a = (tab[i][j] + tab[j][i]) / 2
            mat[i][j], mat[j][i] = a, a
    return np.array(mat)

def getRoomates(matrix, ids, entryOrder=None):
    if entryOrder == None:
        cur.execute('SELECT "name" from "User"')
        entryOrder = cur.fetchall()
        entryOrder = [x[0] for x in entryOrder]

    numbersToNames = dict(zip([x for x in range(len(entryOrder))], entryOrder))

    G = nx.from_numpy_array(averageMatrix(matrix))
    a = nx.max_weight_matching(G, maxcardinality=True)
    named = []
    for item in a:
        named.append((str(ids[item[0]]), str(ids[item[1]])))

    namedDict = {}
    for item in named:
        namedDict[item[0]] = item[1]
        namedDict[item[1]] = item[0]
    return namedDict

def getBestMatches(n, matrix, entryOrder):
    numbersToNames = dict(zip([x for x in range(len(entryOrder))], entryOrder))
    compDict = dict(zip([x for x in range(len(matrix[n]))], matrix[n]))

    numsInOrder = sorted(compDict.items(), key=lambda item: item[1], reverse=True)
    numsInOrder = ([numbersToNames[x[0]] for x in numsInOrder[:-1]])
    return numsInOrder[:5]

def compute_best_match(user_id):
    """Compute compatibility matrix and return best match for given user"""
    cur.execute('SELECT "studentId" FROM "Answers";')
    ids = cur.fetchall()
    ids = [x[0] for x in ids]

    print(f"Computing match for user: {user_id}")
    print(f"Total users in database: {len(ids)}")

    # Use enhanced matrix with Gemini integration
    m = populateMatrix(ids, use_gemini=True, gemini_weight=0.4)

    print(f"Matrix size: {len(m)}x{len(m)}")
    if len(m) == 0:
        return None

    roommates = getRoomates(m, ids)
    print(f"Total pairs found: {len(roommates) // 2}")

    roommate_id = roommates.get(user_id, None)
    if not roommate_id:
        return None

    cur.execute('''
                SELECT u.name
                FROM "User" u
                         JOIN "Answers" a ON u.id = a."userId"
                WHERE a."studentId" = %s;
                ''', (roommate_id,))

    result = cur.fetchone()
    if not result:
        return None

    return {
        "best_match": roommate_id,
        "match_name": result[0]
    }

# --- HTTP Server ---

from http.server import BaseHTTPRequestHandler, HTTPServer

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')

        if len(path_parts) == 2 and path_parts[0] == "roommate":
            user_id = path_parts[1]

            best_match = compute_best_match(user_id)

            if best_match is None:
                self.send_response(404)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = "error: User not found or no matches available"
                self.wfile.write(response.encode("utf-8"))
                return

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = json.dumps(best_match)
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Not Found")

def run_server():
    server = HTTPServer(("0.0.0.0", 8080), MyRequestHandler)
    print("Server started at http://localhost:8080")
    print("Usage: GET /roommate/<student_id>")
    print(f"Gemini integration: {'ENABLED' if GEMINI_ENABLED else 'DISABLED'}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()