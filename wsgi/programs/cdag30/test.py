
import cherrypy

# 這是 MAN 類別的定義
'''
# 在 application 中導入子模組
import programs.cdag30.man as cdag30_man
# 加入 cdag30 模組下的 man.py 且以子模組 man 對應其 MAN() 類別
root.cdag30.man = cdag30_man.MAN()

# 完成設定後, 可以利用
/cdag30/man/assembly
# 呼叫 man.py 中 MAN 類別的 assembly 方法
'''
class Test(object):
    # 各組利用 index 引導隨後的程式執行
    @cherrypy.expose
    def index(self, *args, **kwargs):
        outstring = '''
這是 2014CDA 協同專案下的 cdag30 模組下的 MAN 類別.<br /><br />
<!-- 這裡採用相對連結, 而非網址的絕對連結 (這一段為 html 註解) -->
<a href="assembly">執行  MAN 類別中的 assembly 方法</a><br /><br />
請確定下列零件於 V:/home/lego/man 目錄中, 且開啟空白 Creo 組立檔案.<br />
<a href="/static/lego_man.7z">lego_man.7z</a>(滑鼠右鍵存成 .7z 檔案)<br />
'''
        return outstring

    @cherrypy.expose
    def assembly(self, *args, **kwargs):
        outstring = '''
<!DOCTYPE html> 
<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
</head>
<body>
<script language="JavaScript">
/*設計一個零件組立函示*/
/*
軸面接
axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2)
====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子

constrain_way 參數
1 對齊 對齊
2 對齊 貼合
else 按照 1

plane1~plane2 要組裝的父 參考面
plane3~plane4 要組裝的子 參考面
*/
function axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2) {
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName("v:/home/lego/man/" + part2);
    var componentModel = session.GetModelFromDescr(descr);
    if (componentModel == null) {
        document.write("在session 取得不到零件" + part2);
        componentModel = session.RetrieveModel(descr);
        if (componentModel == null) {
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    if (componentModel != void null) {
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }


    var ids = pfcCreate("intseq");
    //假如  asm 有零件時候
    if (featID != -1) {

        ids.Append(featID);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    }
    // 假如是第一個零件 asm 就當作父零件
    else {
        var subassembly = assembly;
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    if (constrain_way == 1) {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    } else if (constrain_way == 2) {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
    } else {
        var relation = new Array(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);

    }
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
    for (var i = 0; i < 2; i++) {
        var asmItem = subassembly.GetItemByName(relationItem[i], asmDatums[i]);
        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(relationItem[i], compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
        var MpfcSelect = pfcCreate("MpfcSelect");
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(relation[i]);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(true, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    return asmcomp.Id;
}
// 以上為 axis_plane_assembly() 函式
//
function three_plane_assembly(session, assembly, transf, featID, constrain_way, part2, plane1, plane2, plane3, plane4, plane5, plane6) {
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName("v:/home/lego/man/" + part2);
    var componentModel = session.GetModelFromDescr(descr);
    if (componentModel == null) {
        document.write("在session 取得不到零件" + part2);
        componentModel = session.RetrieveModel(descr);
        if (componentModel == null) {
            throw new Error(0, "Current componentModel is not loaded.");
        }
    }
    if (componentModel != void null) {
        var asmcomp = assembly.AssembleComponent(componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    //假如  asm 有零件時候
    if (featID != -1) {

        ids.Append(featID);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        var subassembly = subPath.Leaf;
    }
    // 假如是第一個零件 asm 就當作父零件
    else {
        var subassembly = assembly;
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    }


    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++) {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);

        if (asmItem == void null) {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null) {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        if (constrain_way == 1) {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        } else if (constrain_way == 2) {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        } else {
            var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        }
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create(false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    return asmcomp.Id;
}
// 以上為 three_plane_assembly() 函式
//
// 假如 Creo 所在的操作系統不是 Windows 環境
if (!pfcIsWindows()) {
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
}
// pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
var session = pfcGetProESession();
// 設定 config option, 不要使用元件組立流程中內建的假設約束條件
session.SetConfigOption("comp_placement_assumptions", "no");
// 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
var identityMatrix = pfcCreate("pfcMatrix3D");
// 建立 identity 位置矩陣
for (var x = 0; x < 4; x++) {
    for (var y = 0; y < 4; y++) {
        if (x == y) {
            identityMatrix.Set(x, y, 1.0);
        } else {
            identityMatrix.Set(x, y, 0.0);
        }
    }
}
// 利用 identityMatrix 建立 transf 座標轉換矩陣
var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
// 取得目前的工作目錄
var currentDir = session.getCurrentDirectory();
// 以目前已開檔的空白組立檔案, 作為 model
var model = session.CurrentModel;
// 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error(0, "Current model is not an assembly.");
// 將此模型設為組立物件
var assembly = model;

/*
three_plane_assembly(session, assembly, transf, featID, constrain_way, part2, plane1, plane2, plane3, plane4, plane5, plane6)
=====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子

constrain_way 參數
1 對齊
2 貼合
else 按照 1

plane1~plane3 要組裝的父 參考面
plane4~plane6 要組裝的子 參考面

axis_plane_assembly(session, assembly, transf, featID, constrain_way, part2, axis1, plane1, axis2, plane2)
====================
assembly 組立檔案
transf 座標矩陣
feadID 要組裝的父
part2 要組裝的子

constrain_way 參數
1 對齊 對齊
2 對齊 貼合
else 按照 1

plane1~plane2 要組裝的父 參考面
plane3~plane4 要組裝的子 參考面
*/

var body_id = three_plane_assembly(session, assembly, transf, -1, 1, "LEGO_BODY.prt", "ASM_FRONT", "ASM_TOP", "ASM_RIGHT", "FRONT", "TOP", "RIGHT");

var arm_right_id = axis_plane_assembly(session, assembly, transf, body_id, 2, "LEGO_ARM_RT.prt", "A_14", "DTM1", "A_9", "TOP");

var arm_left_id = axis_plane_assembly(session, assembly, transf, body_id, 2, "lego_arm_lt.prt", "A_15", "DTM2", "A_7", "TOP");

var hand_left_id = axis_plane_assembly(session, assembly, transf, arm_left_id, 1, "lego_hand.prt", "A_8", "DTM1", "A_1", "DTM3");

var hand_right_id = axis_plane_assembly(session, assembly, transf, arm_right_id, 1, "lego_hand.prt", "A_10", "DTM1", "A_1", "DTM3");


var head_id = axis_plane_assembly(session, assembly, transf, body_id, 1, "lego_head.prt", "A_16", "DTM3", "A_2", "DTM1");


var hat_id = axis_plane_assembly(session, assembly, transf, head_id, 1, "lego_hat.prt", "A_2", "TOP", "A_2", "FRONT");

var waist_id = three_plane_assembly(session, assembly, transf, body_id, 1, "LEGO_WAIST.prt", "DTM4", "TOP", "DTM7", "DTM1", "RIGHT", "FRONT");

var leg_left_id = axis_plane_assembly(session, assembly, transf, waist_id, 2, "lego_leg_lt.prt", "A_8", "DTM4", "A_10", "DTM1");
var leg_right_id = axis_plane_assembly(session, assembly, transf, waist_id, 2, "lego_leg_rt.prt", "A_8", "DTM5", "A_10", "DTM1");

assembly.Regenerate(void null);
session.GetModelWindow(assembly).Repaint();
</script></body></html>'''
        return outstring
