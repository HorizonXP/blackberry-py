#undef QT_NO_STL
#undef QT_NO_STL_WCHAR

#ifndef NULL
#define NULL    0
#endif

#define qdoc

#include <QtCore/QVariant>
#include <QVariant>

#include <bb/cascades/AbsoluteLayout>
#include <bb/cascades/AbsoluteLayoutProperties>
#include <bb/cascades/AbstractActionItem>
#include <bb/cascades/AbstractAnimation>
#include <bb/cascades/AbstractButton>
#include <bb/cascades/AbstractPane>
#include <bb/cascades/AbstractTextControl>
#include <bb/cascades/AbstractToggleButton>
#include <bb/cascades/AbstractTransition>
#include <bb/cascades/ActionBarPlacement>
#include <bb/cascades/ActionItem>
#include <bb/cascades/ActionSet>
#include <bb/cascades/ActivityIndicator>
#include <bb/cascades/Application>
#include <bb/cascades/Button>
#include <bb/cascades/CheckBox>
#include <bb/cascades/ChromeVisibility>
#include <bb/cascades/Color>
//#include <bb/cascades/ColorPaint>
#include <bb/cascades/Container>
#include <bb/cascades/ContextMenuHandler>
//#include <bb/cascades/ContextMenuShowingEvent>
#include <bb/cascades/Control>
#include <bb/cascades/CustomControl>
#include <bb/cascades/CustomDialog>
#include <bb/cascades/DataModel>
#include <bb/cascades/DataModelChangeType>
//#include <bb/cascades/DataSetModel>
#include <bb/cascades/DateTimePicker>
#include <bb/cascades/DateTimePickerMode>
#include <bb/cascades/DeleteActionItem>
#include <bb/cascades/DisplayDirection>
#include <bb/cascades/Divider>
#include <bb/cascades/DockLayout>
#include <bb/cascades/DockLayoutProperties>
//#include <bb/cascades/DoubleTapEvent>
#include <bb/cascades/DoubleTapHandler>
#include <bb/cascades/DropDown>
#include <bb/cascades/EasingCurve>
#include <bb/cascades/Event>
#include <bb/cascades/FadeTransition>
#include <bb/cascades/FlowListLayout>
#include <bb/cascades/FlowListLayoutProperties>
#include <bb/cascades/FontStyle>
#include <bb/cascades/FontStyleHint>
#include <bb/cascades/FontWeight>
#include <bb/cascades/ForeignWindow>
#include <bb/cascades/GestureHandler>
#include <bb/cascades/GridListLayout>
#include <bb/cascades/GroupAnimation>
//#include <bb/cascades/GroupDataModel>
#include <bb/cascades/HeaderListItem>
#include <bb/cascades/HelpActionItem>
#include <bb/cascades/HorizontalAlignment>
#include <bb/cascades/Image>
#include <bb/cascades/ImageButton>
//#include <bb/cascades/ImagePaint>
#include <bb/cascades/ImageToggleButton>
//#include <bb/cascades/ImageTracker>
#include <bb/cascades/ImageView>
#include <bb/cascades/ImplicitAnimationController>
#include <bb/cascades/InvokeActionItem>
#include <bb/cascades/InvokeQuery>
#include <bb/cascades/ItemGrouping>
#include <bb/cascades/Label>
#include <bb/cascades/Layout>
#include <bb/cascades/LayoutDirection>
#include <bb/cascades/LayoutProperties>
#include <bb/cascades/LayoutUpdateHandler>
#include <bb/cascades/ListHeaderMode>
#include <bb/cascades/ListItemListener>
#include <bb/cascades/ListItemManager>
#include <bb/cascades/ListItemTypeMapper>
#include <bb/cascades/ListLayout>
#include <bb/cascades/ListView>
//#include <bb/cascades/LongPressEvent>
#include <bb/cascades/LongPressHandler>
#include <bb/cascades/Menu>
#include <bb/cascades/MultiSelectActionItem>
#include <bb/cascades/MultiSelectHandler>
#include <bb/cascades/NavigationPane>
#include <bb/cascades/NavigationPaneProperties>
#include <bb/cascades/Option>
#include <bb/cascades/OrientationSupport>
#include <bb/cascades/OverlapTouch>
#include <bb/cascades/Page>
#include <bb/cascades/PageResizeBehavior>
#include <bb/cascades/Paint>
#include <bb/cascades/PaneProperties>
#include <bb/cascades/ParallelAnimation>
//#include <bb/cascades/PinchEvent>
#include <bb/cascades/PinchHandler>
//#include <bb/cascades/PixelBufferData>
#include <bb/cascades/ProgressIndicator>
#include <bb/cascades/ProgressIndicatorState>
#include <bb/cascades/PropagationPhase>
//#include <bb/cascades/QListDataModel>
#include <bb/cascades/QmlDocument>
#include <bb/cascades/RadioGroup>
#include <bb/cascades/RepeatPattern>
#include <bb/cascades/RotateTransition>
#include <bb/cascades/ScaleTransition>
#include <bb/cascades/ScalingMethod>
#include <bb/cascades/ScrollAnimation>
#include <bb/cascades/ScrollIndicatorMode>
#include <bb/cascades/ScrollMode>
#include <bb/cascades/ScrollView>
#include <bb/cascades/ScrollViewProperties>
#include <bb/cascades/SegmentedControl>
#include <bb/cascades/SequentialAnimation>
#include <bb/cascades/SettingsActionItem>
#include <bb/cascades/Sheet>
#include <bb/cascades/SidebarState>
#include <bb/cascades/Slider>
#include <bb/cascades/StackLayout>
#include <bb/cascades/StackLayoutProperties>
#include <bb/cascades/StackListLayout>
#include <bb/cascades/StandardListItem>
#include <bb/cascades/StockCurve>
#include <bb/cascades/SupportedDisplayOrientation>
#include <bb/cascades/SystemDefaults>
#include <bb/cascades/Tab>
#include <bb/cascades/TabbedPane>
//#include <bb/cascades/TapEvent>
#include <bb/cascades/TapHandler>
#include <bb/cascades/TextAlignment>
//#include <bb/cascades/TextArea>
#include <bb/cascades/TextAreaInputMode>
#include <bb/cascades/TextField>
#include <bb/cascades/TextFieldInputMode>
#include <bb/cascades/TextJustification>
//#include <bb/cascades/TextStyle>
//#include <bb/cascades/TextStyleDefinition>
#include <bb/cascades/TitleBar>
#include <bb/cascades/TitleBarKind>
#include <bb/cascades/ToggleButton>
#include <bb/cascades/TouchBehavior>
//#include <bb/cascades/TouchEnterEvent>
//#include <bb/cascades/TouchEvent>
//#include <bb/cascades/TouchExitEvent>
#include <bb/cascades/TouchPropagationMode>
#include <bb/cascades/TouchReaction>
#include <bb/cascades/TouchResponse>
#include <bb/cascades/TouchType>
#include <bb/cascades/TranslateTransition>
#include <bb/cascades/UiObject>
#include <bb/cascades/UiOrientation>
#include <bb/cascades/VerticalAlignment>
#include <bb/cascades/VisualNode>
#include <bb/cascades/WebLoadRequest>
#include <bb/cascades/WebNavigationRequest>
//#include <bb/cascades/WebResourceRequestFilter>
//#include <bb/cascades/WebSettings>
//#include <bb/cascades/WebView>
#include <bb/cascades/Window>
#include <bb/cascades/XmlDataModel>

