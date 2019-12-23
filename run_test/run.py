import os
import HTMLTestRunner
import unittest

from remind import now_time


# 创建测试目录（报告，图片，日志）
# user_path = 'D:\\'
# report_path = os.path.join(user_path, 'tours_report') if os.path.exists(
#     os.path.join(user_path, 'tours_report')) else os.mkdir(os.path.join(user_path, 'tours_report'))
# if not report_path:
#     report_path = os.path.join(user_path, 'tours_report')
# image_path = os.path.join(report_path, 'images') if os.path.exists(os.path.join(report_path, 'images')) else os.mkdir(
#     os.path.join(report_path, 'images'))
# if not image_path:
#     image_path = os.path.join(report_path, 'images')

if __name__ == '__main__':
    '''引用时，会检验case_ui中的路径信息，在未创建目录时，会报错，故放在创建目录之后'''
    from case import case_ui
    suite = unittest.TestSuite()
    # suite.addTests([case_ui.Tours('test_pc_visitor_create_order'), ])
    suite.addTests([case_ui.Tours('test_pc_custom_create_order'), ])
    # suite.addTests([case_ui.Tours('test_m_visitor_create_order'), ])
    with open('../tours_report/%s.html' % now_time.get_times(), 'wb') as f:
    # with open(os.path.join(report_path,'%s.html' % now_time.get_times()), 'wb') as f:
        run = HTMLTestRunner.HTMLTestRunner(stream=f, description='ui_test_tours_create_order', verbosity=2, title='TourScool')
        run.run(suite)
