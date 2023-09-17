import glob
import os
import logging
import subprocess
import sys


class TruVideo:

    def __init__(
            self,
            dry_run: bool = False,
            verbose: bool = False,
            log_level: str = "INFO",
            source: str = "./",
            overwrite: bool = False,
            config_file: str = "~/.config/truvideo/config.json"
    ):
        self.results = {}
        self.dry_run: bool = dry_run
        self.verbose: bool = verbose
        self.source: str = source
        self.overwrite: bool = overwrite
        self._config_file = None
        self.config_file: str = config_file
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=log_level,
        )
        self.logger: logging.Logger = logging.getLogger(__name__)

    @property
    def config_file(self) -> str:
        return self._config_file

    @config_file.setter
    def config_file(self, value: str):
        if os.path.isfile(os.path.expanduser(value)):
            self._config_file = os.path.expanduser(value)
        else:
            self.logger.error(f"Config file does not exist: {value}")
            sys.exit(1)

    def _is_file_converted(self, video_file: str) -> bool:
        if self.overwrite:
            return False
        return os.path.isfile(video_file.replace(".mkv", ".mp4"))

    def _get_files(self) -> list:
        files = []
        if not os.path.exists(self.source):
            self.logger.error(f"Source does not exist: {self.source}")
        else:
            if os.path.isdir(self.source):
                files = [
                    video_file for video_file in glob.glob(f"{self.source}/*.mkv", recursive=True) if
                    not self._is_file_converted(video_file.replace(".mkv", ".mp4"))
                ]
            elif os.path.isfile(self.source):
                files = [self.source]

        return sorted(files)

    def _convert_file(self, input_file: str):
        output_file = input_file.replace(".mkv", ".mp4")
        params = [
            f"--preset-import-file \"{self.config_file}\"l",
            f"-i \"{input_file}\"",
            f"-o \"{output_file}\"",
            "--subtitle scan",
            "--subtitle-forced",
            "--subtitle-burned",
        ]

        cmd = f"HandBrakeCLI {' '.join(params)}"
        self.logger.info(cmd)

        if not self.dry_run:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout.readlines():
                self.logger.debug(line.strip())
            retval = proc.wait()

            if retval != 0:
                self.logger.error(f"Error converting file: {input_file}")
                self.logger.error(retval)
                return False

        return True

    def run(self):
        self.logger.info(f"Converting files in {self.source}")
        for _file in self._get_files():
            self.results[_file] = self._convert_file(_file)
