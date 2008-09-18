<!-- allows the user to change the interface style and the language-->
<?cs if:((subcount(Config.UI.Interfaces) > 0) && UI.Top.Interface)
		|| ((subcount(Config.UI.Languages) > 0) && UI.Top.Language) ?>

	<?cs call:form_header_ignore("select_interface", "template", "web_lang", "")
	
	?><?cs if:Data.List.Name ?><input type="hidden" name="action"
			value="subscribers" /><?cs /if
			
	?><?cs if:subcount(Config.UI.Languages) > 1 ?>
		<font class="no_link"><?cs
			var:html_escape(Lang.Menue.Language) ?>:</font>
		<select name="web_lang" size="0">
			<?cs each: tlang = Config.UI.Languages
				?><option value="<?cs var:name(tlang) ?>"<?cs
					if:name(tlang) == Config.UI.LinkAttrs.web_lang
					?> selected="selected"<?cs /if?>><?cs
				var:html_escape(tlang) ?></option>
				<?cs /each ?></select><?cs
	else ?>
		<input type="hidden" name="web_lang" value="<?cs
				var:Config.UI.LinkAttrs.web_lang ?>" /><?cs /if
	?><?cs if:subcount(Config.UI.Interfaces) > 1 ?>
		<font class="no_link"><?cs
			var:html_escape(Lang.Menue.Interface) ?>:</font>
		<select name="template" size="0">
			<?cs each: ttemp = Config.UI.Interfaces
				?><option value="<?cs var:name(ttemp) ?>"<?cs
					if:name(ttemp) == Config.UI.LinkAttrs.template
					?> selected="selected"<?cs /if?>><?cs
				var:html_escape(Lang.Misc.Interfaces[ttemp]) ?></option>
				<?cs /each ?></select><?cs
	else ?>
		<input type="hidden" name="template" value="<?cs
				var:Config.UI.LinkAttrs.template ?>" /><?cs /if
	?><button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.InterfaceSet) ?></button>
	</form>

<?cs /if ?>

