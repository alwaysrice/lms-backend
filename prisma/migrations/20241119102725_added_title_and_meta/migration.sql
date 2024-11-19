/*
  Warnings:

  - Added the required column `meta` to the `Group` table without a default value. This is not possible if the table is not empty.
  - Added the required column `meta` to the `Post` table without a default value. This is not possible if the table is not empty.
  - Added the required column `title` to the `Post` table without a default value. This is not possible if the table is not empty.
  - Made the column `user_id` on table `Post` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `meta` to the `Task` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE "Post" DROP CONSTRAINT "Post_user_id_fkey";

-- AlterTable
ALTER TABLE "Group" ADD COLUMN     "meta" JSONB NOT NULL;

-- AlterTable
ALTER TABLE "Post" ADD COLUMN     "meta" JSONB NOT NULL,
ADD COLUMN     "published" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "title" TEXT NOT NULL,
ALTER COLUMN "user_id" SET NOT NULL;

-- AlterTable
ALTER TABLE "Task" ADD COLUMN     "meta" JSONB NOT NULL;

-- CreateTable
CREATE TABLE "_posts_saved" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateTable
CREATE TABLE "_posts_viewed" (
    "A" INTEGER NOT NULL,
    "B" INTEGER NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "_posts_saved_AB_unique" ON "_posts_saved"("A", "B");

-- CreateIndex
CREATE INDEX "_posts_saved_B_index" ON "_posts_saved"("B");

-- CreateIndex
CREATE UNIQUE INDEX "_posts_viewed_AB_unique" ON "_posts_viewed"("A", "B");

-- CreateIndex
CREATE INDEX "_posts_viewed_B_index" ON "_posts_viewed"("B");

-- AddForeignKey
ALTER TABLE "Post" ADD CONSTRAINT "Post_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_posts_saved" ADD CONSTRAINT "_posts_saved_A_fkey" FOREIGN KEY ("A") REFERENCES "Post"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_posts_saved" ADD CONSTRAINT "_posts_saved_B_fkey" FOREIGN KEY ("B") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_posts_viewed" ADD CONSTRAINT "_posts_viewed_A_fkey" FOREIGN KEY ("A") REFERENCES "Post"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "_posts_viewed" ADD CONSTRAINT "_posts_viewed_B_fkey" FOREIGN KEY ("B") REFERENCES "User"("id") ON DELETE CASCADE ON UPDATE CASCADE;
