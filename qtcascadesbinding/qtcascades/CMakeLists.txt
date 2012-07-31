PROJECT(QtCascades)

SET(qtcascades_SRC
	${CMAKE_CURRENT_BINARY_DIR}/PySide/QtCascades/bb_application_wrapper.h
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
	${QNX_TARGET_DIR}/usr/include/bb/cascades/controls
	${QNX_TARGET_DIR}/usr/include/bb/cascades/core
	${QNX_TARGET_DIR}/usr/include/bb/cascades/databinding
	${QNX_TARGET_DIR}/usr/include/bb/cascades/resources
)

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

