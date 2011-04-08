<?php 
//XMLDropper: Aid for creating Second Life client localizations 
	// (by dropping elements)
	//© 2008 Kakurady Drakenar. 
	//Last modified: 2008-07-14
	
//This program is Free Software; you can redistribute it, modify it, or both
	//under the terms of GNU General Public License version 2, or any later 
	//version of the License as you like, as published by Free Software Foundation. ...

//This program is distributed in the hope that it will be useful,
	//but WITHOUT ANY WARRANTY; without even the implied warranty of
	//MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	//GNU General Public License for more details.
	
//You should have received a copy of the GNU General Public License
	//along with this program.  If not, see <http://www.gnu.org/licenses/>.

//Second Life® is a trademark of Linden Research, Inc. Kakurady is not affliated 
	//with or endorsed by Linden Research. No infringement intended.
	
//TODO: File upload, tips 
$debug = false;

$lastnodeiselement = false;
$reader = new XMLReader();

//output and highlight init
$highlight = false;
if (isset($_POST['highlight'])) { $highlight = true; }
$buf = "";
$postdata = "";
if (isset($argv)){
	if (isset($argv[1])){
		$postdata = file_get_contents($argv[1], 'r');
	}
	function output($arg){
		echo ($arg);
	}
} else {
	function output($arg){
		global $highlight;
		global $buf;
		if($highlight){
			$buf .= $arg;
		}else{
			echo htmlspecialchars($arg);
		}
	}

	if(isset($_FILES['catalog']['error']) && $_FILES['catalog']['error'] == UPLOAD_ERR_OK){
		$postdata = file_get_contents($_FILES['catalog']['tmp_name']);
		$posttitle= $_FILES['catalog']['name']; 
	}else{
		$postdata = stripslashes($_POST['text']);

	}
	include_once('../lib/geshi/geshi.php');
	// or else...

	if($highlight){$geshi = new GeSHi($buf, 'xml');
	$geshi->enable_classes();
	$style= $geshi->get_stylesheet(false);
	}
}



$lastdepth = 0;
$drop_depth = 0;
$dropping = false;
$keep = true;

$droppable = array(
	'type',
	'length',
	'allow_text_entry', //combo_box
	'allow_html',
	'auto_resize',
	'bevel_style',
	'background_opaque',
	'background_visible',
	'bg_alpha_color',
	'bg_opaque_color',
	'bg_readonly_color',
	'bg_writeable_color',
	'bg_visible',
	'border',
	'border_color',
	'border_drop_shadow_visible',
	'border_style',
	'border_visible',
	'border_thickness',
	'handle_edit_keys_directly',
	'bottom',
	'bottom_delta',
	'can_apply_immediately',
	'can_close',
	'can_drag_on_left',
	'can_edit_text',
	'can_minimize',
	'can_resize',
	'can_tearoff',
	'color',
	'column_padding',
	'control_name',
	'create_jump_keys',
	'decimal_digits',
	'default_tab_group',
	'drop_shadow',
	'drop_shadow_visible',
	'draw_border', //radio_group
	'draw_heading',
	'draw_stripes',
	'dynamicwidth',
	'embedded_items',
	'enabled',
	'follows',
	'font',
	'function',
	'h_pad',
	'halign',
	'height',
	'hidden',
	'hide_border',
	'hide_scrollbar',
	'image_name',
	'image_overlay',
	'image_selected',
	'image_unselected',
	'initial_val',
	'initial_value',
	'label_width',
	'layout', //panel
	'left',
	'left_delta',
	'image_overlay_alignment',
	'increment',
	'max_chars', //combo_box
	'max_length',
	'max_val',
	'min_val',
	'min_width', //floater
	'min_height', //floater
	'mouse_opaque',
	'multi_select',
	'opaque',
	'orientation',
	'radio_style',
	'rect_control',
	'right',
	'scale_image',
	'search_column',
	'select_all_on_focus_received',
	'select_on_focus',
	'shortcut', //menu_item_*
	'show_text',
	'sort',
	'sort_column',//scroll_list
	'tab_group',
	'tab_position',
	'tab_stop',
	'tear_off',
	'text_color',
	'text_readonly_color',
	'top',
	'top_delta',
	'user_resize',
	'userdata',
	'v_pad',
	'volume',
	'width',
	'word_wrap'
);

$droppable_elements =  array(
	'menu_item_separator',
	'on_click',
	'on_check',
	'on_enable',
	
	//viewer 2 stuff
    'commit_callback',
    'button.commit_callback',
	'line_editor.commit_callback',
	'menu_item_call.on_click',
	'menu_item_check.on_check',
    'menu_item_check.on_enable',
    'panel_camera_item.mousedown_callback',
    'panel_camera_item.picture',
    'panel_camera_item.selected_picture',

    'mouse_held_callback',
	    //notifications
	'tag',
);

$reader->XML($postdata);
if(!isset($argv)){
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="text/html; charset=utf-8" http-equiv="content-type" /><title><?php
	echo (isset($posttitle))? $posttitle :'posted XML';  
?> :: XMLDropper</title>

<style type="text/css">
h1 {
font-family: DejaVu Sans;
font-weight: bold;
border-bottom-style: dotted;
border-bottom-width: 3pt;
font-size: 20pt;
}
h2 {
font-family: DejaVu Sans;
font-weight: bold;
border-bottom-width: 2pt;
border-bottom-style: dashed;
font-size: 17pt;
font-style: normal;
}

<?php echo $style; ?>

</style>
  <link rel="shortcut icon" type="image/vnd.microsoft.icon" href="/nekotoba_icon.ico">
  <link rel="icon" type="image/png" href="/nekotoba_icon.png">
</head>
<body>

<?php
}
// app logic

if(!$highlight && !isset($argv)){echo "<pre>";}

$lastelementname = "";
output('<?xml version="1.0" encoding="utf-8" standalone="yes" ?>'."\n");
while ($reader->read()){
	
	if ($lastnodeiselement){
		if ($reader->depth > $lastdepth){ 	// does not self-close; has children
			output(">");	
		}else{ 		
								// self-closing
			if ($reader->nodeType ==  XMLReader::END_ELEMENT){
				//if($reader->name == $lastelementname){
						output(">");	
				//} //else {
				//		output(">");	
				//}
			} else {
				output(" />");	
			}
		}
		$lastnodeiselement = false;
	}
	
	$lastdepth = $reader->depth;
	if ($dropping){
		if ($reader->depth > $droppingdepth){
			continue;
		} else if ($reader->nodeType == XMLReader::END_ELEMENT){
			$dropping = false;
			continue;
		} else {
			$dropping = false;
		}
	}
	switch ($reader->nodeType){
		case XMLReader::ELEMENT:
			if (in_array($reader->name, $droppable_elements)) { 
				//drop element, and subelements (if any)
				$dropping = true;
				$droppingdepth = $reader->depth;
				break; 
			}
			
			output(sprintf("<%s", $reader -> name));
			
			while ($reader -> moveToNextAttribute()){
				//would be quicker if use a hash table!
				if (!in_array($reader->name, $droppable)){
					output(sprintf ('%s%s %s="%s"', "\n", str_repeat  ( "\t"  , $reader->depth),  $reader->name, htmlspecialchars($reader->value)));
				}
			}	
			$lastnodeiselement = true;
			$lastelementname = $reader->name;
			break;
		case XMLReader::END_ELEMENT:
			//if (in_array($reader->name, $droppable_elements)) { break; }
			
			output(sprintf("</%s>", $reader -> name));
			break;
		case XMLReader::COMMENT:
			output(sprintf('<!--%s-->', $reader -> value));
			break;
		default:
			if ($debug && !$highlight){
				switch ($reader->nodeType){
					case XMLReader::TEXT: 
						echo '<!--TEXT-->'; break;
					case XMLReader::WHITESPACE: 
						echo '<!--WHITESPACE-->'; break;
					case XMLReader::SIGNIFICANT_WHITESPACE:
						echo '<!--SIGNIFICANT_WHITESPACE-->'; break;
				}
			}
			output(htmlspecialchars($reader -> value));
	}
	
	
	
}


if(!isset($argv)){
if(!$highlight){echo "</pre>";
}else{
	$geshi->set_source($buf);
	echo $geshi->parse_code();
}

?>

</body>
</html>
<?php } else { ?>

<?php } //final white line ?>
