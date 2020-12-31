from src.Application import Application


def main():
    # Run application staff.
    import sys
    sys.setrecursionlimit(10000)

    app = Application()
    app.run()

    return 0


if __name__ == "__main__":
    main()

