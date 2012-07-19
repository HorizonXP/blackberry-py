PROJECT(QtCascades)

SET(qtcascades_SRC
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/qtcascades_module_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_application_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_abstractpane_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_application_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_datamodel_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_qmldocument_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_qmldocument_builder_wrapper.cpp
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_cascades_uiobject_wrapper.cpp
)

SET(qtcascades_INCLUDE_DIRECTORIES
	${SHIBOKEN_INCLUDE_DIR}
	${PYTHON_INCLUDE_PATH}
	${PYSIDE_INCLUDE_DIR}
	${PYSIDE_INCLUDE_DIR}/QtCore
	/home/micke/dev/stage/include/PySide/QtGui
	/home/micke/dev/stage/include/PySide/QtNetwork
	/home/micke/dev/stage/include/PySide/QtDeclarative
	${QT_INCLUDE_DIR}
	${QT_QTCORE_INCLUDE_DIR}
	${QT_INCLUDE_DIR}/QtNetwork
	${QT_INCLUDE_DIR}/QtDeclarative
	${QNX_TARGET_DIR}/usr/include
	${QNX_TARGET_DIR}/usr/include/bb/core
	${QNX_TARGET_DIR}/usr/include/bb/cascades
	${QNX_TARGET_DIR}/usr/include/bb/cascades/controls
	${QNX_TARGET_DIR}/usr/include/bb/cascades/core
	${QNX_TARGET_DIR}/usr/include/bb/cascades/databinding
	${QNX_TARGET_DIR}/usr/include/bb/cascades/resources
)
MESSAGE("${qtcascades_INCLUDE_DIRECTORIES}")

SET(qtcascades_LINK_LIBRARIES
	${QT_QTCORE_LIBRARY}
	/home/micke/dev/libpython3.2m.so.1.0
	/home/micke/dev/libshiboken.cpython-32mu.so.1.1
	/home/micke/dev/libpyside.cpython-32mu.so.1.1
	libQtCascades.so
)

INCLUDE_DIRECTORIES(
	QtCascades
	${qtcascades_INCLUDE_DIRECTORIES}
	/home/micke/dev/stage/include/PySide
	/home/micke/dev/stage/include/PySide/QtCore
)
ADD_LIBRARY(QtCascades MODULE ${qtcascades_SRC})
SET_PROPERTY(TARGET QtCascades PROPERTY PREFIX "")
TARGET_LINK_LIBRARIES(QtCascades ${qtcascades_LINK_LIBRARIES})
ADD_DEFINITIONS(
	#-L/home/micke/Documents/dev/libs/bbndk-10.0.4-beta/lib
	#-L/home/micke/Documents/dev/libs/bbndk-10.0.4-beta/target/qnx6/armle-v7/usr/lib
)

ADD_CUSTOM_COMMAND(OUTPUT ${qtcascades_SRC}
	COMMAND shiboken
	--enable-parent-ctor-heuristic --enable-pyside-extensions --enable-return-value-heuristic
	${CMAKE_SOURCE_DIR}/qtcascades/global.h
	--include-paths=${QT_INCLUDE_DIR}:${QNX_TARGET_DIR}/usr/include
	--typesystem-paths=${typesystem_path}:/home/micke/dev/stage/share/PySide/typesystems
	--output-directory=${CMAKE_CURRENT_BINARY_DIR}
#	--debug-level=full
	${CMAKE_CURRENT_SOURCE_DIR}/typesystem_qtcascades.xml
	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
	COMMENT "Running generator for libqtcascades..."
)

