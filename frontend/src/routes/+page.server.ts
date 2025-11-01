import type { Actions } from './$types';
import {prisma} from "$lib/server/prisma";
import {redirect} from "@sveltejs/kit";



export const actions = {
    default: async ({request}) => {
        console.log("Attempting to send data")
        const data = await request.formData()
        formToDatabase(data);
        redirect(303, '/results');
    }
} satisfies Actions;

function formToDatabase(data: FormData): void {


    const workStartTimeString = data.get("work-start") as string;
    const workEndTimeString = data.get("work-end") as string;
    const nightOutBedtimeString = data.get("night-out-bedtime") as string;
    const normalWeekdayBedtimeString = data.get("normal-weekday-bedtime") as string;
    const normalWeekdayStartTimeString = data.get("normal-weekday-waketime") as string;
    const tidinessString = data.get("tidiness") as string;
    const careAboutTidinessString = data.get("care-about-tidiness") as string;
    const sportsWatchedString = data.get("sports-watched") as string;
    const sportsPlayedString = data.get("sports-played") as string;
    const musicGenresString = data.get("music-genres") as string;
    const musicArtistsString = data.get("music-artists") as string;

    const name = data.get("name") as string;
    const studentId = data.get("student-id") as string;
    const gender = data.get("gender") as string;
    const workStartTime = Number.parseInt(workStartTimeString);
    const workEndTime = Number.parseInt(workEndTimeString);
    const nightOutBedtime = Number.parseInt(nightOutBedtimeString);
    const normalWeekdayBedtime = Number.parseInt(normalWeekdayBedtimeString);
    const normalWeekdayStartTime = Number.parseInt(normalWeekdayStartTimeString);
    const overnightGuests = data.get("overnight-guests") as string;
    const introvertExtrovert = data.get("introvert-extrovert") as string;
    const tidiness = Number.parseInt(tidinessString);
    const careAboutTidiness = Number.parseInt(careAboutTidinessString);
    const sportsWatched = sportsWatchedString.split(",")
    const sportsPlayed = sportsPlayedString.split(",")
    const musicGenres = musicGenresString.split(",")
    const musicArtists = musicArtistsString.split(",")
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
