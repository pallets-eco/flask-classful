import nose


if __name__ == "__main__":
    # nose.run()
    nose.run(env={
        'NOSE_INCLUDE_EXE': True,
        'NOSE_VERBOSE': 2
    })
