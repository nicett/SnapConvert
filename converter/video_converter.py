import ffmpeg
import os
import logging
from converter.base_converter import Converter


class VideoConverter(Converter):
    def convert_file(self, file_path, output_path):
        pass

    def __init__(self, input_files, output_folder, target_format, progress_var, progress_label, progress_manager):
        super().__init__(input_files, output_folder, target_format, progress_var, progress_label)
        self.input_files = input_files
        self.output_folder = output_folder
        self.target_format = target_format
        self.progress_var = progress_var
        self.progress_label = progress_label
        self.progress_manager = progress_manager

    def convert(self):
        total_files = len(self.input_files)
        for i, file_path in enumerate(self.input_files):
            try:

                base_name = os.path.basename(file_path)
                output_path = os.path.join(self.output_folder, os.path.splitext(base_name)[0] + f'.{self.target_format.lower()}')
                # 检查文件是否已存在，并生成唯一文件名
                output_path = self.get_unique_filename(output_path)
                ffmpeg.input(file_path).output(output_path,crf=0).run()

                # 更新进度条
                self.progress_manager.update_progress(self.progress_var, self.progress_label, i, total_files)

            except Exception as e:
                logging.error(f"转换失败: {file_path}，错误: {str(e)}")
                continue

    def update_progress(self, current_index):
        """
        更新进度条
        :param current_index:
        :return:
        """
        progress_percentage = (current_index + 1) / self.total_files * 100
        self.progress_var.set(progress_percentage)
        self.progress_label.config(text=f"{progress_percentage:.2f}%")