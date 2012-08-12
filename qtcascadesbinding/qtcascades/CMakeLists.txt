PROJECT(QtCascades)

SET(qtcascades_SRC
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_application_wrapper.h
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/qtcascades_module_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_application_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_wrapper.cpp

	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_absolutelayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_absolutelayoutproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstractactionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstractanimation_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstractbutton_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstractgestureevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstractpane_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstracttextcontrol_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstracttogglebutton_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstracttransition_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_actionbarplacement_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_actionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_actionset_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_activityindicator_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_application_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_button_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_checkbox_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_chromevisibility_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_color_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_colorpaint_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_container_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_contextmenuhandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_contextmenushowingevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_control_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_customcontrol_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_customdialog_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_datamodel_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_datamodelchangetype_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_datasetmodel_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_datetimepicker_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_datetimepickermode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_deleteactionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_displaydirection_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_divider_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_docklayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_docklayoutproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_doubletapevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_doubletaphandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_dropdown_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_easingcurve_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_event_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_fadetransition_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_flowlistlayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_flowlistlayoutproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_fontstyle_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_fontstylehint_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_fontweight_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_foreignwindow_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_gesturehandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_gridlistlayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_groupanimation_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_groupdatamodel_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_headerlistitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_helpactionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_horizontalalignment_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_image_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_imagebutton_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_imagepaint_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_imagetogglebutton_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_imagetracker_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_imageview_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_implicitanimationcontroller_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_invokeactionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_invokequery_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_itemgrouping_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_label_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_layout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_layoutdirection_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_layoutproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_layoutupdatehandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_listheadermode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_listitemlistener_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_listitemmanager_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_listitemtypemapper_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_listlayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_listview_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_longpressevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_longpresshandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_menu_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_multiselectactionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_multiselecthandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_navigationpane_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_navigationpaneproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_option_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_orientationsupport_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_overlaptouch_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_page_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_pageresizebehavior_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_paint_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_paneproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_parallelanimation_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_pinchevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_pinchhandler_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_pixelbufferdata_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_progressindicator_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_progressindicatorstate_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_propagationphase_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_qlistdatamodel_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_qmldocument_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_qmldocument_builder_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_radiogroup_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_repeatpattern_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_resource_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_rotatetransition_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scaletransition_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scalingmethod_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scrollanimation_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scrollindicatormode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scrollmode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scrollview_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_scrollviewproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_segmentedcontrol_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_sequentialanimation_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_settingsactionitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_sheet_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_sidebarstate_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_slider_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_stacklayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_stacklayoutproperties_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_stacklistlayout_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_standardlistitem_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_stockcurve_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_supporteddisplayorientation_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_systemdefaults_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_tab_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_tabbedpane_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_tapevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_taphandler_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textalignment_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textarea_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textareainputmode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textfield_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textfieldinputmode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textjustification_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textstyle_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_textstyledefinition_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_titlebar_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_titlebarkind_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_togglebutton_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchbehavior_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchenterevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchexitevent_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchpropagationmode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchreaction_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchresponse_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_touchtype_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_translatetransition_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_uiobject_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_uiorientation_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_verticalalignment_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_visualnode_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_webloadrequest_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_webnavigationrequest_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_webresourcerequestfilter_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_websettings_wrapper.cpp
	#${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_webview_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_window_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_xmldatamodel_wrapper.cpp
)

SET(qtcascades_INCLUDE_DIRECTORIES
	${SHIBOKEN_INCLUDE_DIR}
	${PYTHON_INCLUDE_PATH}
	${PYSIDE_INCLUDE_DIR}
	${PYSIDE_INCLUDE_DIR}/QtCore
	${PYSIDE_INCLUDE_DIR}/QtGui
	${PYSIDE_INCLUDE_DIR}/QtNetwork
	${PYSIDE_INCLUDE_DIR}/QtDeclarative
	${QT_INCLUDE_DIR}
	${QT_QTCORE_INCLUDE_DIR}
	${QT_INCLUDE_DIR}/QtNetwork
	${QT_INCLUDE_DIR}/QtDeclarative
	${QNX_TARGET_DIR}/usr/include
	${QNX_TARGET_DIR}/usr/include/bb/core
	${QNX_TARGET_DIR}/usr/include/bb/cascades
	${QNX_TARGET_DIR}/usr/include/bb/cascades/animation
	${QNX_TARGET_DIR}/usr/include/bb/cascades/controls
	${QNX_TARGET_DIR}/usr/include/bb/cascades/core
	${QNX_TARGET_DIR}/usr/include/bb/cascades/databinding
	${QNX_TARGET_DIR}/usr/include/bb/cascades/layouts
	${QNX_TARGET_DIR}/usr/include/bb/cascades/resources
	${QNX_TARGET_DIR}/usr/include/bb/cascades/web
)

SET(qtcascades_LINK_LIBRARIES
	${QT_QTCORE_LIBRARY}
	/home/micke/dev/libpython3.2m.so.1.0
	/home/micke/dev/libshiboken.cpython-32mu.so.1.1
	/home/micke/dev/libpyside.cpython-32mu.so.1.1
	libbbcascades.so
)

INCLUDE_DIRECTORIES(
	QtCascades
	${qtcascades_INCLUDE_DIRECTORIES}
)
ADD_LIBRARY(QtCascades MODULE ${qtcascades_SRC} ${CMAKE_BINARY_DIR}/file_patched)
SET_PROPERTY(TARGET QtCascades PROPERTY PREFIX "")
TARGET_LINK_LIBRARIES(QtCascades ${qtcascades_LINK_LIBRARIES})

ADD_CUSTOM_COMMAND(OUTPUT ${qtcascades_SRC}
	DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/typesystem_qtcascades.xml
	DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/global.h
	COMMAND shiboken
	--enable-parent-ctor-heuristic --enable-pyside-extensions --enable-return-value-heuristic
	${CMAKE_SOURCE_DIR}/qtcascades/global.h
	--include-paths=${QT_INCLUDE_DIR}:${QNX_TARGET_DIR}/usr/include
	--typesystem-paths=${typesystem_path}:/home/micke/dev/stage/share/PySide/typesystems
	--output-directory=${CMAKE_CURRENT_BINARY_DIR}
	${CMAKE_CURRENT_SOURCE_DIR}/typesystem_qtcascades.xml
	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
	COMMENT "Running generator for libqtcascades..."
)


# This is a hacky workaround until we have a proper solution to this:
# https://bugreports.qt-project.org/browse/PYSIDE-101
SET_SOURCE_FILES_PROPERTIES(${CMAKE_BINARY_DIR}/file_patched PROPERTIES SYMBOLIC True)
ADD_CUSTOM_COMMAND(OUTPUT ${CMAKE_BINARY_DIR}/file_patched
	DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_application_wrapper.h
	COMMAND patch -p1 < ${CMAKE_CURRENT_SOURCE_DIR}/namespace-workaround.patch
	COMMAND touch file_patched
	WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
	COMMENT "Patching header files"
)

