import operations_course as oc
import operations_gui as og
import operations_class as ocl
import operations_profs as op
import Prof

profs_info = op.load_profs()
course_info = oc.load_courses()
classes_info = ocl.load_classes()


og.show_root_page()

op.save_profs(profs_info)
oc.save_courses(course_info)
ocl.save_classes(classes_info)
