<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- message size limit -->
<input type="checkbox" name="msgsize_min_state"
	value="selected" id="msgsize_min_state" <?cs
	if:Data.List.MsgSize.Min>0 ?>checked="checked"<?cs /if ?> />
	<label for="msgsize_min_state"><?cs var:html_escape(Lang.Misc.MessageSize.Min) ?></label>
	<ul><li><input type="text" name="msgsize_min_value" size="10"
	style="text-align:right" value="<?cs
	alt:Data.List.MsgSize.Min ?>2<?cs /alt ?>" /> <?cs
	var:html_escape(Lang.Misc.MessageSize.Unit) ?></li></ul>
