/*
  Warnings:

  - You are about to drop the column `groupId` on the `Task` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `Task` table. All the data in the column will be lost.
  - Made the column `group_id` on table `Post` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `creatorId` to the `Task` table without a default value. This is not possible if the table is not empty.
  - Added the required column `userId` to the `TaskSubmission` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "Post" DROP CONSTRAINT "Post_group_id_fkey";

-- DropForeignKey
ALTER TABLE "Post" DROP CONSTRAINT "Post_user_id_fkey";

-- DropForeignKey
ALTER TABLE "Task" DROP CONSTRAINT "Task_groupId_fkey";

-- DropForeignKey
ALTER TABLE "Task" DROP CONSTRAINT "Task_userId_fkey";

-- AlterTable
ALTER TABLE "Post" ADD COLUMN     "desc" TEXT,
ALTER COLUMN "user_id" DROP NOT NULL,
ALTER COLUMN "group_id" SET NOT NULL;

-- AlterTable
ALTER TABLE "Task" DROP COLUMN "groupId",
DROP COLUMN "userId",
ADD COLUMN     "creatorId" INTEGER NOT NULL;

-- AlterTable
ALTER TABLE "TaskSubmission" ADD COLUMN     "userId" INTEGER NOT NULL;

-- CreateTable
CREATE TABLE "_GroupToTask" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateTable
CREATE TABLE "_assigned_users" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "_GroupToTask_AB_unique" ON "_GroupToTask"("A", "B");

-- CreateIndex
CREATE INDEX "_GroupToTask_B_index" ON "_GroupToTask"("B");

-- CreateIndex
CREATE UNIQUE INDEX "_assigned_users_AB_unique" ON "_assigned_users"("A", "B");

-- CreateIndex
CREATE INDEX "_assigned_users_B_index" ON "_assigned_users"("B");

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_group_id_fkey" FOREIGN KEY ("group_id") REFERENCES "Group"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Task" ADD CONSTRAINT "Task_creatorId_fkey" FOREIGN KEY ("creatorId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TaskSubmission" ADD CONSTRAINT "TaskSubmission_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_GroupToTask" ADD CONSTRAINT "_GroupToTask_A_fkey" FOREIGN KEY ("A") REFERENCES "Group"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_GroupToTask" ADD CONSTRAINT "_GroupToTask_B_fkey" FOREIGN KEY ("B") REFERENCES "Task"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_assigned_users" ADD CONSTRAINT "_assigned_users_A_fkey" FOREIGN KEY ("A") REFERENCES "Task"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_assigned_users" ADD CONSTRAINT "_assigned_users_B_fkey" FOREIGN KEY ("B") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
