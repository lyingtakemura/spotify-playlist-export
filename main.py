import logging

from spotify import ExportToCSV, ExportToJSON, Spotify

logging.basicConfig(format='%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d \
:: %(message)s', level=logging.DEBUG)


def main():
    spotify = Spotify()
    spotify.get_playlist()
    spotify.export_playlist(ExportToCSV())
    spotify.export_playlist(ExportToJSON())


if __name__ == "__main__":
    logging.debug(main)
    main()
