import ffmpeg
import os
import logging

class VideoConverter:
    def __init__(self, input_files, output_folder, target_format, progress_var, progress_label, progress_manager):
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
                ffmpeg.input(file_path).output(output_path).run()

                # 更新进度条
                self.progress_manager.update_progress(self.progress_var, self.progress_label, i, total_files)

            except Exception as e:
                logging.error(f"转换失败: {file_path}，错误: {str(e)}")
                continue
