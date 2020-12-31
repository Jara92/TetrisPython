from src.CApplication import CApplication


def main():
    # Run application staff.
    import sys
    sys.setrecursionlimit(10000)

    app = CApplication()
    app.run()

    return 0


if __name__ == "__main__":
    main()

