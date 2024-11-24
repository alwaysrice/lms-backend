-- DropForeignKey
ALTER TABLE "TaskSubmission" DROP CONSTRAINT "TaskSubmission_user_draft_id_fkey";

-- AlterTable
ALTER TABLE "TaskSubmission" ALTER COLUMN "user_draft_id" DROP NOT NULL;

-- AddForeignKey
ALTER TABLE "TaskSubmission" ADD CONSTRAINT "TaskSubmission_user_draft_id_fkey" FOREIGN KEY ("user_draft_id") REFERENCES "User"("id") ON DELETE SET NULL ON UPDATE CASCADE;
