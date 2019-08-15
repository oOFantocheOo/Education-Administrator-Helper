import Class
import Course
import operations_breaktime as ob
import operations_class as ocl
import operations_course as oc
import operations_gui as og
import operations_profs as op
import operations_settings as ost

profs_info = op.load_profs()
course_info = oc.load_courses()
classes_info = ocl.load_classes()
break_time_info = ob.load_breaktime()
settings = ost.load_settings()

og.show_root_page(profs_info, course_info, classes_info, break_time_info, settings)

op.save_profs(profs_info)
oc.save_courses(course_info)
ocl.save_classes(classes_info)
ob.save_breaktime(break_time_info)
ost.save_settings(settings)
