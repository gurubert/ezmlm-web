<?cs def:help_title(helpname)
	?>title="<?cs alt:Lang.Helper[helpname] ?>TODO: unknown helpname (<?cs
	var:helpname ?>)<?cs /alt ?>"<?cs
 /def ?>

<?cs def:checkbox(option)
	?><?cs if:Lang.Options[option]
		?><input type="checkbox" name="option_<?cs var:option ?>" value="selected" <?cs if:(Data.List.Options[option] == 1) ?>checked="checked"<?cs /if ?> />&nbsp;<?cs var:html_escape(Lang.Options[option]) ?><?cs
		set:available_options = available_options + option ?><?cs
	else ?>unknown option (<?cs var:option ?>)<?cs /if ?><?cs
 /def ?>

<?cs def:setting(setting)
	?><?cs if:Lang.Settings[setting]
		?><input type="checkbox" name="setting_state_<?cs var:setting ?>"
			value="selected" <?cs if:(Data.List.Settings[setting].state == 1)
			?>checked="checked"<?cs
			/if ?> />&nbsp;<?cs var:html_escape(Lang.Settings[setting]) ?>
		<ul><li><input type="text" name="setting_value_<?cs var:setting ?>" value="<?cs
			var:html_escape(Data.List.Settings[setting].value) ?>" size="30" /></li></ul><?cs
		set:available_settings = available_settings + setting ?><?cs
	else ?>unknown setting (<?cs var:setting ?>)<?cs /if ?><?cs
 /def ?>

<?cs def:warning(warnname)
    ?><div class="warning">
		<?cs alt:Lang.WarningMessage[warnname] ?>unknown warning message (<?cs
		var:warnname ?>)<?cs /alt ?>
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

