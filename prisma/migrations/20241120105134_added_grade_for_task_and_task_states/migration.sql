-- CreateEnum
CREATE TYPE "TaskStateType" AS ENUM ('COMPLETED', 'MISSED', 'DUE');

-- AlterTable
ALTER TABLE "TaskSubmission" ADD COLUMN     "grade" INTEGER;

-- CreateTable
CREATE TABLE "TaskState" (
    "id" SERIAL NOT NULL,
    "source_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "state" "TaskStateType" NOT NULL,

    CONSTRAINT "TaskState_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "TaskState" ADD CONSTRAINT "TaskState_source_id_fkey" FOREIGN KEY ("source_id") REFERENCES "Task"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TaskState" ADD CONSTRAINT "TaskState_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
