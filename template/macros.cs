<?cs def:help_icon(helpname)
	?>&nbsp;<img src="<?cs var:HelpIconURL ?>" title="<?cs alt:Lang.Helper[helpname]
	?>unknown helpname (<?cs var:helpname ?><?cs /alt ?>"/><?cs
 /def ?>

<?cs def:help_title(helpname)
	?>title="<?cs alt:Lang.Helper[helpname] ?>TODO: unknown helpname (<?cs
	var:helpname ?>)<?cs /alt ?>"<?cs
 /def ?>

<?cs def:generic_icon(helptext)
	?>&nbsp<img src="<?cs var:HelpIconURL ?>" title="<?cs var:helptext ?>"/><?cs
 /def ?>

<?cs def:checkbox(option)
	?><?cs if:Lang.Options[option]
		?><input type="checkbox" name="option_<?cs var:option ?>" value="selected" <?cs if:(Data.List.Options[option] == 1) ?>checked="checked"<?cs /if ?> />&nbsp; <?cs var:Lang.Options[option] ?><?cs
		set:available_options = available_options + option ?><?cs
	else ?>unknown checkbox (<?cs var:option ?>)<?cs /if ?><?cs
 /def ?>

<?cs def:warning(warnname)
    ?><div class="warning">
		<?cs alt:Lang.WarningMessage[warname] ?>unknown warning message (?cs
		var:warname ?>)<?cs /alt ?>
	</div><?cs
/def ?>

<?cs def:error(errname)
    ?><div class="error">
		<?cs alt:Lang.ErrorMessage[errname] ?>unknown error message (<?cs
		var:errname ?>)<?cs /alt ?>
	</div><?cs
/def ?>

<?cs def:success(succname)
    ?><div class="success">
		<?cs alt:Lang.SuccessMessage[succname] ?>unknown success message (<?cs 
		var:succname ?>)<?cs /alt ?>
	</div><?cs
/def ?>

