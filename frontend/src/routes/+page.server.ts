import type {Actions} from './$types';
import {prisma} from "$lib/server/prisma";
import {redirect} from "@sveltejs/kit";
import {error} from "@sveltejs/kit";

export const actions = {
    default: async ({request}) => {
        const data = await request.formData();

        function getNum(key: string) {
            const num = Number.parseInt(data.get(key) as string);
            if (isNaN(num)) {
                error(403,"Invalid number");
            }
            return num;
        }

        function getTags(key: string) {
            let jsonData: any;
            try {
                jsonData = JSON.parse(data.get(key) as string);
            } catch {
                error(403, "Invalid data");
            }
            if (!Array.isArray(jsonData)) {
                error(403, "Invalid data");
            }
            for (const item of jsonData) {
                if (typeof item !== "string") {
                    error(403, "Invalid data");
                }
            }
            return jsonData;
        }

        function getString(key: string) {
            const str = data.get(key) as string | null;
            if (str == null) {
                error(403,"Invalid string");
            }
            return str;
        }
        
        const name = getString("name");
        const studentId = getString("student-id");
        const gender = getString("gender");
        const workStartTime = getNum("work-start");
        const workEndTime = getNum("work-end");
        const nightOutBedtime = getNum("night-out-bedtime");
        const normalWeekdayBedtime = getNum("normal-weekday-bedtime");
        const normalWeekdayStartTime = getNum("normal-weekday-waketime");
        const overnightGuests = getString("overnight-guests");
        const introvertExtrovert = getString("introvert-extrovert");
        const tidiness = getNum("care-about-tidiness");
        const careAboutTidiness = getNum("tidiness");
        const sportsWatched = getTags("sports-watched");
        const sportsPlayed = getTags("sports-played");
        const musicGenres = getTags("music-genres");
        const musicArtists = getTags("music-artists");
        const idealRoommate = getString("ideal-roommate-description");
        const selfDescription = getString("self-description");

        prisma.user.create({
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
        }).then();
        redirect(303, '/results');
    }
} satisfies Actions;
