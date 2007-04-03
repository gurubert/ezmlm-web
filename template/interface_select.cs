<!-- allows the user to change the interface language (not of the list!) -->
<?cs if:subcount(Config.UI.Interfaces) > 0 ?>

	<?cs call:form_header("select_interface", "template") ?>

		<?cs if:Data.List.Name ?><input type="hidden" name="action"
				value="subscribers" /><?cs /if ?>

		<font class="no_link"><?cs
			var:html_escape(Lang.Menue.Interface) ?>:</font><br/>
		<select name="template" size="0">
			<?cs each: ttemp = Config.UI.Interfaces
				?><option value="<?cs var:name(ttemp) ?>"<?cs
					if:name(ttemp) == Config.UI.LinkAttrs.template
					?> selected="selected"<?cs /if?>><?cs
				var:html_escape(Lang.Misc.Interfaces[ttemp]) ?></option>
				<?cs /each ?>
		</select>&nbsp;<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.InterfaceSet) ?></button>
	</form>

<?cs /if ?>
