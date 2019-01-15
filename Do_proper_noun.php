<?php
header("Content-Type:text/html; charset=utf-8");

require_once(dirname(__FILE__) . "/config.php");

function uploadfile($file_id,$uploaddir,$file_name){

  if (!file_exists($uploaddir)){
    mkdir($uploaddir);
  }
  if ($_FILES[$file_id]['error'] === UPLOAD_ERR_OK){

    # 檢查檔案是否已經存在
    if (file_exists($uploaddir. $file_name)){
      echo '檔案已覆蓋。<br/>';
      unlink($uploaddir. $file_name);
    } 
    $file = $_FILES[$file_id]['tmp_name'];
    $dest = $uploaddir . $file_name;
    # 將檔案移至指定位置
    move_uploaded_file($file, $dest);
    
  } else {
   echo '錯誤代碼：' . $_FILES[$file_id]['error'] . '未上傳檔案或字典<br/>';

  }
}
function exec_time($timeN,$timeP){
    $time = strtotime($timeN) - strtotime($timeP); 
    $n_time = str_pad(floor($time/3600/24),2,0,STR_PAD_LEFT )."天".str_pad(floor($time%(24*3600)/3600),2,0,STR_PAD_LEFT )."小時".str_pad(floor($time%3600/60),2,0,STR_PAD_LEFT)."分".str_pad($time%3600%60, 2, 0, STR_PAD_LEFT)."秒";
    return $n_time;
}

$timenamefolder=date("YmdHis").rand(0,100);
$uploaddir = './excel_document/'.$timenamefolder.'/';

if (!file_exists('excel_document/')){
    mkdir('excel_document/');
}

uploadfile('excel_file',$uploaddir,$_FILES['excel_file']['name']);
uploadfile('proper_file',$uploaddir,$_FILES['proper_file']['name']);
$excel_content = $_POST['excel_content'];
$keyword = $_POST['keyword'];

$data = "{\"excel_file\":\"".$_FILES['excel_file']['name']."\",\"excel_content\":\"$excel_content\",\"keyword\":\"$keyword\",\"proper_file\":\"".$_FILES['proper_file']['name']."\"}";
file_put_contents( $uploaddir.'excel_category.json' , $data);
echo 1;
echo exec('python ./call_pn.py '.$timenamefolder.'  2>error.txt 2>&1',$arr,$ret);

echo '<br />'."<button  type=\"button\" onclick=\"location.href='./output/output".$timenamefolder."/output.csv'\">下載專有名詞</button>".'<br />'.'<br />';
$a = shell_exec('python ./del_file.py '.$timenamefolder);
?>