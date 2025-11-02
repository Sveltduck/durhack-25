-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Answers" (
    "userId" INTEGER NOT NULL,
    "EarliestWorkTime" INTEGER NOT NULL,
    "LatestWorkTime" INTEGER NOT NULL,
    "NightOutSleepTime" INTEGER NOT NULL,
    "QuietWeekdaySleepTime" INTEGER NOT NULL,
    "NormalWeekdayWakeUpTime" INTEGER NOT NULL,
    "RoommateOvernightStay" INTEGER NOT NULL,
    "Introverted" INTEGER NOT NULL,
    "SportsWatched" TEXT[],
    "SportsPlayed" TEXT[],
    "MusicGenres" TEXT[],
    "MusicArtists" TEXT[],
    "Tidyness" INTEGER NOT NULL,
    "RoommatesTidyness" INTEGER NOT NULL,
    "IdealRoomate" TEXT NOT NULL,
    "SelfDescription" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Answers_userId_key" ON "Answers"("userId");

-- AddForeignKey
ALTER TABLE "Answers" ADD CONSTRAINT "Answers_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
