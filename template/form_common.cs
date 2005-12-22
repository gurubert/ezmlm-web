<!-- this file should be included in every form with checkboxes and settings -->

<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />

<!-- "available_options" is filled by the checkbox macro -->
<input type="hidden" name="options_available" value="<?cs var:available_options ?>" />
<!-- "available_settings" is filled by the setting macro -->
<input type="hidden" name="settings_available" value="<?cs var:available_settings ?>" />
	
