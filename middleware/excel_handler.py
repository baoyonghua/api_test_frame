import openpyxl
from common.baseexcel import BaseExcel
from common.baselogger import logger
from config.pyfile_path import PyConfig


class ExcelHandler(BaseExcel):
    @staticmethod
    def write_excel(sheet_name, row, column, data):
        """
        写入excel
        """
        try:
            wb = openpyxl.load_workbook(PyConfig.excel_path)
            sheet = wb[sheet_name]
        except Exception as e:
            logger.error("打开excel失败")
            raise e
        cell = sheet.cell(row, column)
        cell.value = data
        wb.save(PyConfig.excel_path)
        logger.info("写入excel {}成功，数据：{}".format(sheet_name, data))


excel_handler = ExcelHandler(PyConfig.excel_path)

# if __name__ == '__main__':
#     data = excel_handler.read_excel('registe')
#     # data = excel_handler.get_title('registe')
#     print(data)
