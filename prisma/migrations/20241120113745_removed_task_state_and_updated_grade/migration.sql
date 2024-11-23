/*
  Warnings:

  - You are about to drop the `TaskState` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropForeignKey
ALTER TABLE "TaskState" DROP CONSTRAINT "TaskState_source_id_fkey";

-- DropForeignKey
ALTER TABLE "TaskState" DROP CONSTRAINT "TaskState_user_id_fkey";

-- DropTable
DROP TABLE "TaskState";

-- DropEnum
DROP TYPE "TaskStateType";

-- CreateTable
CREATE TABLE "TaskResponse" (
    "id" SERIAL NOT NULL,
    "source_id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "graded_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "remark" TEXT,
    "grade" INTEGER,
    "attachments" TEXT[],

    CONSTRAINT "TaskResponse_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "TaskResponse" ADD CONSTRAINT "TaskResponse_source_id_fkey" FOREIGN KEY ("source_id") REFERENCES "Task"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "TaskResponse" ADD CONSTRAINT "TaskResponse_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
