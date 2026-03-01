import a_thread, a_logger


def adder():
    a_logger.log.write("Value Logged")
    return 1+1

def subtractor():
    a_logger.log.write("subtractor", tag="SUB")
    return 1-1


if __name__ == "__main__":
    a_thread.run(adder, "thread_1", "i", 1000)
    a_thread.run(subtractor, "thread_2", "i", 1000)

    while (a_thread.running("thread_1") and a_thread.running("thread_2") ):
        continue
    a_logger.log.save(file_name="LOGA")
    a_logger.log.save(file_name="LOGB",log_category="SUB")