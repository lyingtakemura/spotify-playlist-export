import logging
import sys

from spotify import ExportToCSV, ExportToJSON, Spotify

logging.basicConfig(
    format="%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s",
    level=logging.DEBUG,
)


def main():
    try:
        spotify = Spotify()
        spotify.get_playlist()

        if "--csv" in sys.argv:
            spotify.export_playlist(ExportToCSV())

        if "--json" in sys.argv:
            spotify.export_playlist(ExportToJSON())

    except KeyboardInterrupt:
        print("\nINTERRUPTED")


if __name__ == "__main__":
    logging.debug(main)
    main()
