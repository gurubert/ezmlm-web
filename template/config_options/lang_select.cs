<!-- REMOVE --><?cs include:TemplateDir + '/macros.cs' ?>
<!-- list language -->
<?cs if:subcount(Data.List.AvailableLanguages) > 0 ?>
	<label for="list_language"><?cs var:html_escape(Lang.Misc.ListLanguage)
			?>:</label>
		<select name="list_language" id="list_language">
			<?cs each:item = Data.List.AvailableLanguages ?>
				<option <?cs if:(item == Data.List.Language)
					?>selected="selected"<?cs /if ?>><?cs var:item ?></option>
			<?cs /each ?>
		</select><?cs /if ?>
