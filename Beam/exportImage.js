/**** This file saves the current display in high resolution to a file  ****/

main("C:/Users/vinicius/AppData/Local/Temp/WB_FLWS008_vinicius_6952_3/unsaved_project_files/user_files/test.png");

function main(fileName)
{
    // Zoom to Fit
    DS.Graphics.Camera.zoomFit();

    //get the active item in the tree
    var curResult = DS.Tree.FirstActiveObject;
    var nodeID = curResult.ID;

    if( !curResult )
        return;

    var ch_png = "File PNG (*.png)|*.png|";
    var ch_jpg = "File JPEG (*.jpg)|*.jpg|";
    var ch_tif = "File TIFF (*.tif)|*.tif|";
    var ch_bmp = "File BMP (*.bmp)|*.bmp|";
    var ch_eps = "File EPS (*.eps)|*.eps|";
    var filter = ch_png + ch_jpg + ch_tif + ch_bmp + ch_eps;

    var fName = fileName;
    
    var png = /.png$/i;   // $=end of string,  i=case insensitive
    var jpg = /.jpg$/i;
    var tif = /.tif$/i;
    var bmp = /.bmp$/i;
    var eps = /.eps$/i;
    var imode = 0;

    if (fName.search(png) > -1) imode = 0;
    if (fName.search(jpg) > -1) imode = 1;
    if (fName.search(tif) > -1) imode = 2;
    if (fName.search(bmp) > -1) imode = 3;
    if (fName.search(eps) > -1) imode = 4;

    var width  = WB.PreferenceMgr.Preference("PID_Report_Graphics_Figure_Width");
    var height = WB.PreferenceMgr.Preference("PID_Report_Graphics_Figure_Height");
    var imgEnhance = WB.PreferenceMgr.Preference("PID_Report_Figure_Resolution");

    DS.Graphics.MemStreamWidth  = width * imgEnhance;
    DS.Graphics.MemStreamHeight = height * imgEnhance;    // Pixel Height
    
    DS.Graphics.StreamMode = 1;    // 0=normal, 1=mem
    var WCC_BEGIN = 1;
    var WCC_END = 2;
    WB.DoWaitCursor( WCC_BEGIN );
    
    //font height of 16 looks too big when printed.  use 12
    DS.Graphics.SetFontStyle( 0, "Arial", 0, 0, 14*imgEnhance, 0, 0 );
    var imageCtrl = DS.Graphics.ImageCaptureControl;
    DS.Graphics.Draw2 (nodeID);
    imageCtrl.Write( imode, fName );
    
    DS.Graphics.SetFontStyle( 0, "Arial", 0, 0, 16, 0, 0 );
    DS.Graphics.StreamMode = 0; // 0=normal, 1=mem
    DS.Graphics.Draw2 (nodeID);
        
    WB.DoWaitCursor( WCC_END );
}