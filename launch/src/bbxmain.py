import sys
import datetime

def main():
    try:
        with open('shared/documents/bbxrun.log', 'a') as outf:
            sys.stdout = sys.stderr = outf
            print('-' * 40)
            print('start:', datetime.datetime.now())
            print('args:', ' '.join(sys.argv))

            try:
                sys.path.insert(1, 'shared/documents')
                import bbxrun
                bbxrun.run()

            except:
                import traceback
                traceback.print_exc()

            finally:
                print('done:', datetime.datetime.now())

    finally:
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    main()
