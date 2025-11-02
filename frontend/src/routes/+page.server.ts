import type {Actions} from './$types';
import {prisma} from "$lib/server/prisma";
import {redirect} from "@sveltejs/kit";
import {error} from "@sveltejs/kit";


export const actions = {
    default: async ({request}) => {
        console.log("Attempting to send data")
        const data = await request.formData()
        await formToDatabase(data);
        redirect(303, '/results');
    }
} satisfies Actions;

function parseNum(data: FormDataEntryValue | null) {
    const num = Number.parseInt(data as string);
    if (isNaN(num)) {
        error(403,"Invalid number")
    }
    return num
}

function parseList(data: FormDataEntryValue | null) {
    let jsonData: any
    try {
        jsonData = JSON.parse(data as string);
    } catch {
        console.log(data);
        error(403, "Invalid data")
    }
    if (!Array.isArray(jsonData)) {
        error(403, "Invalid data")
    }
    for (const item of jsonData) {
        if (typeof item !== "string") {
            error(403, "Invalid data: string list contains non string value")
        }
    }
    return jsonData;
}

function parseString(data: FormDataEntryValue | null) {
    const str = data as string;
    if (str == null) {
        error(403,"Invalid string")
    }
    return str;
}

async function formToDatabase(data: FormData): Promise<void> {
    const name = parseString(data.get("name"))
    const studentId = parseString(data.get("student-id"))
    const gender = parseString(data.get("gender"))
    const workStartTime = parseNum(data.get("work-start"));
    const workEndTime = parseNum(data.get("work-end"));
    const nightOutBedtime = parseNum(data.get("night-out-bedtime"));
    const normalWeekdayBedtime = parseNum(data.get("normal-weekday-bedtime"));
    const normalWeekdayStartTime = parseNum(data.get("normal-weekday-waketime"));
    const overnightGuests = parseString(data.get("overnight-guests"))
    const introvertExtrovert = parseString(data.get("introvert-extrovert"))
    const tidiness = parseNum(data.get("care-about-tidiness"));
    const careAboutTidiness = parseNum(data.get("tidiness"));
    const sportsWatched = parseList(data.get("sports-watched"));
    const sportsPlayed = parseList(data.get("sports-played"));
    const musicGenres = parseList(data.get("music-genres"));
    const musicArtists = parseList(data.get("music-artists"));
    const idealRoommate = parseString(data.get("ideal-roommate-description"))
    const selfDescription = parseString(data.get("self-description"))

    try {
        await prisma.user.create({
            data: {
                name,
                answers: {
                    create: {
                        studentId,
                        gender,
                        workStartTime,
                        workEndTime,
                        nightOutBedtime,
                        normalWeekdayBedtime,
                        normalWeekdayStartTime,
                        overnightGuests,
                        introvertExtrovert,
                        tidiness,
                        careAboutTidiness,
                        sportsWatched,
                        sportsPlayed,
                        musicGenres,
                        musicArtists,
                        idealRoommate,
                        selfDescription,
                    }
                }
            }
        })
    } catch {
        error(403, "Invalid data")
    }
    console.log("data sent");
}
