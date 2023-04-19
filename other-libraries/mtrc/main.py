import sys
import os
import shutil
import pandas as pd
from PySide6 import QtWidgets, QtCore
from qt_material import apply_stylesheet

from display import Ui_Dialog
from help import idx_to_cata, find_certain_line, insert_certain_lines


class displayWindow(QtWidgets.QWidget, Ui_Dialog):

    def __init__(self):
        super(displayWindow, self).__init__()
        self.setupUi(self)
        self.excel_add_btn.clicked.connect(self.get_excel_file_name)
        self.udf_folder_add_btn.clicked.connect(self.get_udf_folder_name)
        self.output_folder_add_btn.clicked.connect(self.get_output_folder_name)
        self.information_clear_btn.clicked.connect(self.clear_information)
        self.task_start_btn.clicked.connect(self.process)

        self.maintain_mode_selection.addItems(['添加', '覆盖'])

        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.home_path = os.getcwd()
        self.name_count = {100: 0, 200: 0, 400: 0, 600: 0}

    def get_excel_file_name(self):
        file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', self.home_path, 'Excel文件(*.xls *.xlsx);;所有文件(*)')
        self.excel_line_edit.setText(file_name)

    def get_udf_folder_name(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, '选择文件夹', self.home_path)
        self.udf_folder_line_edit.setText(folder_name)

    def get_output_folder_name(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, '选择文件夹', 'D:/PTC/pro_stds/MTRC_dir/')
        self.output_folder_line_edit.setText(folder_name)

    def clear_information(self):
        self.information_text_browser.clear()

    def process(self):
        maintain_mode = self.maintain_mode_selection.currentText()

        excel_file_path = os.path.normpath(self.excel_line_edit.text())
        udf_folder_path = os.path.normpath(self.udf_folder_line_edit.text())
        output_folder_path = os.path.normpath(self.output_folder_line_edit.text())

        output_udf_dir = os.path.join(output_folder_path, 'Frame_custom_dir')
        text_dir = os.path.join(output_folder_path, 'text')
        icon_msg_file = os.path.join(text_dir, 'IconMessage.txt')

        # 说明：
        # 100-200 小特征
        # 201-400 门面框架
        # 401-600 控盒框架
        # 601-999 小模块
        self.catalog_relation = {'小特征': 100, '门面框架': 201, '控盒框架': 401, '小模块': 601}
        self.name_count = {100: 0, 201: 0, 401: 0, 601: 0}

        if maintain_mode == '添加':
            if os.path.exists(output_udf_dir):
                output_folder_list_raw = os.listdir(output_udf_dir)
                output_folder_list = list(filter(lambda x: os.path.isdir(os.path.join(output_udf_dir, x)) and x.isnumeric(), output_folder_list_raw))
                output_folder_list.sort(key=lambda x: int(x))

                for folder in output_folder_list:
                    cata = idx_to_cata(int(folder))
                    if cata != -1:
                        self.name_count[cata] = int(folder) - cata + 1
            else:
                os.mkdir(output_udf_dir)

            if not os.path.exists(text_dir):
                os.mkdir(text_dir)
            if not os.path.exists(icon_msg_file):
                msg_title = '''Function
UserFunction
MTRC
#


'''
                with open(icon_msg_file, 'a') as f2:
                    f2.write(msg_title)

        elif maintain_mode == '覆盖':
            if os.path.exists(output_udf_dir):
                shutil.rmtree(output_udf_dir)
            os.mkdir(output_udf_dir)

            if not os.path.exists(text_dir):
                os.mkdir(text_dir)
            msg_title = '''Function
UserFunction
MTRC
#


'''
            with open(icon_msg_file, 'a') as f2:
                f2.seek(0)
                f2.truncate()
                f2.write(msg_title)

        try:
            df = pd.read_excel(excel_file_path)
        except:
            self.information_text_browser.append('请检查Excel文件的格式是否设置正确')
            self.information_text_browser.append('------------------------------------------------------------')
        else:
            try:
                df.dropna(axis=0, subset=['No'], inplace=True)
                df.sort_values(by=['No'], ascending=True, inplace=True)
            except:
                self.information_text_browser.append('请检查Excel表格的内容是否符合要求')
                self.information_text_browser.append('------------------------------------------------------------')
            else:
                udf_list = []
                bmp_list = []
                icon_list = []
                udf_folder_list = os.listdir(udf_folder_path)
                for file in udf_folder_list:
                    if '.gph' in file or '.GPH' in file:
                        udf_list.append(file)
                    elif '.bmp' in file or '.BMP' in file:
                        bmp_list.append(file)
                    elif '.png' in file or '.PNG' in file:
                        icon_list.append(file)
                try:
                    udf_list.sort(key=lambda x: int(x[:3]))
                    bmp_list.sort(key=lambda x: int(x[:3]))
                    icon_list.sort(key=lambda x: int(x[:3]))
                except:
                    self.information_text_browser.append('请检查UDF相关文件的命名是否符合要求')
                    self.information_text_browser.append('------------------------------------------------------------')
                else:
                    error_info = self.write_udf_files(df, udf_list, bmp_list, icon_list, udf_folder_path, output_udf_dir, icon_msg_file)
                    total_num = df.shape[0]
                    error_num = len(error_info)
                    self.information_text_browser.append(f'尝试写入UDF{total_num}个，其中成功{total_num - error_num}/{total_num}个，失败{error_num}/{total_num}个')
                    if error_num > 0:
                        self.information_text_browser.append('失败信息如下：')
                        for n in range(error_num):
                            self.information_text_browser.append(f'错误{n + 1}：UDF文件编号为{error_info[n][0]}，错误信息为{error_info[n][1]}')
                    self.information_text_browser.append('------------------------------------------------------------')

    def write_udf_files(self, df, udf_list, bmp_list, icon_list, udf_folder_path, output_udf_dir, icon_msg_file):
        total_line = df.shape[0]
        error_info = []
        for i in range(total_line):
            df_row = df.iloc[i]

            no = df_row['No']
            catalog_name = df_row['Catalog']
            if pd.isnull(catalog_name):
                error_info.append((no, 'CATALOG参数缺失'))
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue
            try:
                catalog = self.catalog_relation[catalog_name]
            except:
                error_info.append((no, 'CATALOG没有按照规定的选项选择'))
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            idx = int(catalog + self.name_count[catalog])
            self.name_count[catalog] += 1

            dir_name = os.path.join(output_udf_dir, str(idx))
            if os.path.exists(dir_name) or idx >= 1000:
                error_info.append((no, '同类型UDF库编号已满'))
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue
            os.mkdir(dir_name)

            udf = udf_list[i]
            icon = icon_list[i]
            bmp = bmp_list[i]
            if no != int(udf[:3]) or no != int(icon[:3]) or no != int(bmp[:3]):
                error_info.append((no, 'UDF相关文件编号不匹配'))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            try:
                udf_old_name = os.path.join(udf_folder_path, udf)
                udf_new_name = os.path.join(dir_name, f'UDF_{idx}.gph.1')
                shutil.copyfile(udf_old_name, udf_new_name)
            except:
                error_info.append((no, 'UDF文件拷贝错误'))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            try:
                icon_old_name = os.path.join(udf_folder_path, icon)
                icon_new_name = os.path.join(dir_name, f'UDF_{idx}.png')
                shutil.copyfile(icon_old_name, icon_new_name)
            except:
                error_info.append((no, '图标PNG文件拷贝错误'))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            try:
                bmp_old_name = os.path.join(udf_folder_path, bmp)
                bmp_new_name = os.path.join(dir_name, f'UDF_{idx}.bmp')
                shutil.copyfile(bmp_old_name, bmp_new_name)
            except:
                error_info.append((no, '说明图片BMP文件拷贝错误'))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            try:
                self.write_ini_file(df_row, idx, dir_name)
            except ValueError as e:
                error_info.append((no, str(e)))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue
            except:
                error_info.append((no, 'INI文件写入错误'))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            try:
                self.write_msg_file(df_row, idx, icon_msg_file)
            except ValueError as e:
                error_info.append((no, str(e)))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue
            except:
                error_info.append((no, 'TXT文件写入错误'))
                shutil.rmtree(dir_name)
                self.name_count[catalog] -= 1
                self.progress_bar.setValue(int((i + 1) / total_line * 100))
                continue

            self.progress_bar.setValue(int((i + 1) / total_line * 100))

        return error_info

    def write_msg_file(self, row, idx, icon_msg_file):
        name = row['Name']
        if pd.isnull(name):
            raise ValueError('MSG文件提示信息缺失')

        msg_template_list = [
            f'{idx}\n',
            f'{name}\n',
            '#\n',
            '#\n',
            '\n',
            f'{idx}_MSG\n',
            f'{name}\n',
            '#\n',
            '#\n',
            '\n',
        ]

        with open(icon_msg_file, 'r+') as f2:
            content_list = f2.readlines()
            pos = find_certain_line(content_list, f'{idx - 1}_MSG')
            if pos > -1:
                content_list = insert_certain_lines(pos + 5, content_list, msg_template_list)
            else:
                cata = idx_to_cata(idx)
                if cata == -1:
                    raise ValueError('UDF文件编号越界')

                done = False
                while not done:
                    if cata == 100:
                        content_list = insert_certain_lines(6, content_list, msg_template_list)
                        done = True
                    elif cata == 201:
                        if self.name_count[100] > 0:
                            prev_pos = find_certain_line(content_list, f'{100 + self.name_count[100] - 1}_MSG')
                            content_list = insert_certain_lines(prev_pos + 5, content_list, msg_template_list)
                            done = True
                        else:
                            cata = 100
                    elif cata == 401:
                        if self.name_count[201] > 0:
                            prev_pos = find_certain_line(content_list, f'{201 + self.name_count[201] - 1}_MSG')
                            content_list = insert_certain_lines(prev_pos + 5, content_list, msg_template_list)
                            done = True
                        else:
                            cata = 201
                    else:
                        content_list.extend(msg_template_list)
                        done = True
            f2.seek(0)
            f2.truncate()
            f2.writelines(content_list)

    def write_ini_file(self, row, idx, dir_name):
        d1, d1_value, d1_x, d1_y = '', '', '', ''
        if not pd.isnull(row['D1']):
            if pd.isnull(row['D1_Value']) or pd.isnull(row['D1_X']) or pd.isnull(row['D1_Y']):
                raise ValueError('D1相关参数缺失')
            d1 = row['D1']
            d1_value = row['D1_Value']
            d1_x = row['D1_X']
            d1_y = row['D1_Y']

        d2, d2_value, d2_x, d2_y = '', '', '', ''
        if not pd.isnull(row['D2']):
            if pd.isnull(row['D2_Value']) or pd.isnull(row['D2_X']) or pd.isnull(row['D2_Y']):
                raise ValueError('D2相关参数缺失')
            d2 = row['D2']
            d2_value = row['D2_Value']
            d2_x = row['D2_X']
            d2_y = row['D2_Y']

        d3, d3_value, d3_x, d3_y = '', '', '', ''
        if not pd.isnull(row['D3']):
            if pd.isnull(row['D3_Value']) or pd.isnull(row['D3_X']) or pd.isnull(row['D3_Y']):
                raise ValueError('D3相关参数缺失')
            d3 = row['D3']
            d3_value = row['D3_Value']
            d3_x = row['D3_X']
            d3_y = row['D3_Y']

        d4, d4_value, d4_x, d4_y = '', '', '', ''
        if not pd.isnull(row['D4']):
            if pd.isnull(row['D4_Value']) or pd.isnull(row['D4_X']) or pd.isnull(row['D4_Y']):
                raise ValueError('D4相关参数缺失')
            d4 = row['D4']
            d4_value = row['D4_Value']
            d4_x = row['D4_X']
            d4_y = row['D4_Y']

        ini_template = f'''[Path]
BMP_Path=D:\\\\PTC\\\\pro_stds\\\\MTRC_dir\\\\Frame_custom_dir\\\\{idx}\\\\udf_{idx}.bmp
UDF_Path=D:\\\\PTC\\\\pro_stds\\\\MTRC_dir\\\\Frame_custom_dir\\\\{idx}\\\\udf_{idx}.gph.1
IconGifPath=D:\\\\PTC\\\\pro_stds\\\\MTRC_dir\\\\Frame_custom_dir\\\\{idx}\\\\udf_{idx}.png

[dimensions_01]
dimensions01={d1}
dimensions01_value={d1_value}
dimensions01_positionX={d1_x}
dimensions01_positionY={d1_y}

[dimensions_02]
dimensions02={d2}
dimensions02_value={d2_value}
dimensions02_positionX={d2_x}
dimensions02_positionY={d2_y}

[dimensions_03]
dimensions03={d3}
dimensions03_value={d3_value}
dimensions03_positionX={d3_x}
dimensions03_positionY={d3_y}

[dimensions_04]
dimensions04={d4}
dimensions04_value={d4_value}
dimensions04_positionX={d4_x}
dimensions04_positionY={d4_y}
'''

        ini_name = os.path.join(dir_name, f'UDF_{idx}.ini')
        with open(ini_name, 'a') as f1:
            f1.seek(0)
            f1.truncate()
            f1.write(ini_template)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = displayWindow()
    # ui.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
    ui.setFixedSize(ui.width(), ui.height())
    apply_stylesheet(app, theme='dark_teal.xml')
    ui.show()
    sys.exit(app.exec_())
