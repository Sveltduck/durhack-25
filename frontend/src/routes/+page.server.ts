import type { Actions } from './$types';
import {prisma} from "$lib/server/prisma";



export const actions = {
    default: async ({request}) => {
        console.log("Attempting to send data")
        const data = await request.formData()
        formToDatabase(data);
    }
} satisfies Actions;

function parseNum(data: FormDataEntryValue | null) {
    return Number.parseInt(data as string);
}

function parseList(data: FormDataEntryValue | null) {
    return data
        ? (data as string).split(",").map(s => s.trim()).filter(Boolean)
        : [];
}

function formToDatabase(data: FormData): void {
    const name = data.get("name") as string;
    const studentId = data.get("student-id") as string;
    const gender = data.get("gender") as string;
    const workStartTime = parseNum(data.get("work-start"));
    const workEndTime = parseNum(data.get("work-end"));
    const nightOutBedtime = parseNum(data.get("night-out-bedtime"));
    const normalWeekdayBedtime = parseNum(data.get("normal-weekday-bedtime"));
    const normalWeekdayStartTime = parseNum(data.get("normal-weekday-waketime"));
    const overnightGuests = data.get("overnight-guests") as string;
    const introvertExtrovert = data.get("introvert-extrovert") as string;
    const tidiness = parseNum(data.get("care-about-tidiness"));
    const careAboutTidiness = parseNum(data.get("tidiness"));
    const sportsWatched = parseList(data.get("sports-watched"));
    const sportsPlayed = parseList(data.get("sports-played"));
    const musicGenres = parseList(data.get("music-genres"));
    const musicArtists = parseList(data.get("music-artists"));
    const idealRoommate = data.get("ideal-roommate-description") as string;
    const selfDescription = data.get("self-description") as string;


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
    }).then()
    console.log("data sent");
}
