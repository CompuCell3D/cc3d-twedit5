import sys
from cc3d.twedit5.__main__ import main, except_hook


if __name__ == '__main__':

    # enable it during debugging in pycharm
    sys.excepthook = except_hook

    main(sys.argv[1:])
