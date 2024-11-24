/*
  Warnings:

  - You are about to drop the column `parentId` on the `Comment` table. All the data in the column will be lost.
  - You are about to drop the column `createdAt` on the `PostReaction` table. All the data in the column will be lost.
  - You are about to drop the column `postId` on the `PostReaction` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `PostReaction` table. All the data in the column will be lost.
  - You are about to drop the column `creatorId` on the `Task` table. All the data in the column will be lost.
  - You are about to drop the column `parentId` on the `TaskComment` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `TaskSubmission` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[user_id,post_id,reaction]` on the table `PostReaction` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `year_start` to the `Group` table without a default value. This is not possible if the table is not empty.
  - Added the required column `post_id` to the `PostReaction` table without a default value. This is not possible if the table is not empty.
  - Added the required column `user_id` to the `PostReaction` table without a default value. This is not possible if the table is not empty.
  - Added the required column `creator_id` to the `Task` table without a default value. This is not possible if the table is not empty.
  - Added the required column `type` to the `Task` table without a default value. This is not possible if the table is not empty.
  - Added the required column `user_draft_id` to the `TaskSubmission` table without a default value. This is not possible if the table is not empty.
  - Added the required column `user_id` to the `TaskSubmission` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "PostViewType" AS ENUM ('Grid', 'List');

-- CreateEnum
CREATE TYPE "SexType" AS ENUM ('MALE', 'FEMALE');

-- DropForeignKey
ALTER TABLE "Comment" DROP CONSTRAINT "Comment_parentId_fkey";

-- DropForeignKey
ALTER TABLE "PostReaction" DROP CONSTRAINT "PostReaction_postId_fkey";

-- DropForeignKey
ALTER TABLE "PostReaction" DROP CONSTRAINT "PostReaction_userId_fkey";

-- DropForeignKey
ALTER TABLE "Task" DROP CONSTRAINT "Task_creatorId_fkey";

-- DropForeignKey
ALTER TABLE "TaskComment" DROP CONSTRAINT "TaskComment_parentId_fkey";

-- DropForeignKey
ALTER TABLE "TaskSubmission" DROP CONSTRAINT "TaskSubmission_userId_fkey";

-- DropIndex
DROP INDEX "PostReaction_userId_postId_reaction_key";

-- AlterTable
ALTER TABLE "Comment" DROP COLUMN "parentId",
ADD COLUMN     "parent_id" INTEGER;

-- AlterTable
ALTER TABLE "Group" ADD COLUMN     "year_end" TIMESTAMP(3),
ADD COLUMN     "year_start" TIMESTAMP(3) NOT NULL;

-- AlterTable
ALTER TABLE "Notification" ADD COLUMN     "meta" JSONB NOT NULL DEFAULT '{}';

-- AlterTable
ALTER TABLE "PostReaction" DROP COLUMN "createdAt",
DROP COLUMN "postId",
DROP COLUMN "userId",
ADD COLUMN     "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN     "post_id" INTEGER NOT NULL,
ADD COLUMN     "user_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "Profile" ADD COLUMN     "address" TEXT,
ADD COLUMN     "birthday" TIMESTAMP(3),
ADD COLUMN     "country" TEXT,
ADD COLUMN     "cover" TEXT,
ADD COLUMN     "links" TEXT[],
ADD COLUMN     "mobile" TEXT,
ADD COLUMN     "religion" TEXT,
ADD COLUMN     "sex" "SexType",
ALTER COLUMN "bio" DROP NOT NULL;

-- AlterTable
ALTER TABLE "Task" DROP COLUMN "creatorId",
ADD COLUMN     "creator_id" INTEGER NOT NULL,
ADD COLUMN     "type" TEXT NOT NULL;

-- AlterTable
ALTER TABLE "TaskComment" DROP COLUMN "parentId",
ADD COLUMN     "parent_id" INTEGER;

-- AlterTable
ALTER TABLE "TaskResponse" ADD COLUMN     "allow_peek" BOOLEAN NOT NULL DEFAULT true;

-- AlterTable
ALTER TABLE "TaskSubmission" DROP COLUMN "userId",
ADD COLUMN     "published" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "user_draft_id" INTEGER NOT NULL,
ADD COLUMN     "user_id" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "meta" JSONB NOT NULL DEFAULT '{}',
ADD COLUMN     "middlename" TEXT,
ADD COLUMN     "suffix" TEXT;

-- CreateTable
CREATE TABLE "UserSettings" (
    "id" SERIAL NOT NULL,
    "user_id" INTEGER NOT NULL,
    "media_view" "PostViewType" NOT NULL DEFAULT 'List',

    CONSTRAINT "UserSettings_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "SiteTheme" (
    "id" SERIAL NOT NULL,
    "settings_id" INTEGER NOT NULL,

    CONSTRAINT "SiteTheme_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ProfileBadge" (
    "id" SERIAL NOT NULL,
    "profile_id" INTEGER NOT NULL,
    "image" TEXT NOT NULL,

    CONSTRAINT "ProfileBadge_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PostTag" (
    "id" SERIAL NOT NULL,
    "post_id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "color" TEXT,

    CONSTRAINT "PostTag_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "_posts_drafted" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "UserSettings_user_id_key" ON "UserSettings"("user_id");

-- CreateIndex
CREATE UNIQUE INDEX "SiteTheme_settings_id_key" ON "SiteTheme"("settings_id");

-- CreateIndex
CREATE UNIQUE INDEX "ProfileBadge_profile_id_key" ON "ProfileBadge"("profile_id");

-- CreateIndex
CREATE UNIQUE INDEX "_posts_drafted_AB_unique" ON "_posts_drafted"("A", "B");

-- CreateIndex
CREATE INDEX "_posts_drafted_B_index" ON "_posts_drafted"("B");

-- CreateIndex
CREATE UNIQUE INDEX "PostReaction_user_id_post_id_reaction_key" ON "PostReaction"("user_id", "post_id", "reaction");

-- AddForeignKey
ALTER TABLE "UserSettings" ADD CONSTRAINT "UserSettings_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "SiteTheme" ADD CONSTRAINT "SiteTheme_settings_id_fkey" FOREIGN KEY ("settings_id") REFERENCES "UserSettings"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ProfileBadge" ADD CONSTRAINT "ProfileBadge_profile_id_fkey" FOREIGN KEY ("profile_id") REFERENCES "Profile"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PostTag" ADD CONSTRAINT "PostTag_post_id_fkey" FOREIGN KEY ("post_id") REFERENCES "Post"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Task" ADD CONSTRAINT "Task_creator_id_fkey" FOREIGN KEY ("creator_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TaskSubmission" ADD CONSTRAINT "TaskSubmission_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TaskSubmission" ADD CONSTRAINT "TaskSubmission_user_draft_id_fkey" FOREIGN KEY ("user_draft_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Comment" ADD CONSTRAINT "Comment_parent_id_fkey" FOREIGN KEY ("parent_id") REFERENCES "Comment"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TaskComment" ADD CONSTRAINT "TaskComment_parent_id_fkey" FOREIGN KEY ("parent_id") REFERENCES "TaskComment"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PostReaction" ADD CONSTRAINT "PostReaction_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PostReaction" ADD CONSTRAINT "PostReaction_post_id_fkey" FOREIGN KEY ("post_id") REFERENCES "Post"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_posts_drafted" ADD CONSTRAINT "_posts_drafted_A_fkey" FOREIGN KEY ("A") REFERENCES "Post"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_posts_drafted" ADD CONSTRAINT "_posts_drafted_B_fkey" FOREIGN KEY ("B") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
