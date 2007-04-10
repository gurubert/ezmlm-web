<fieldset>
	<legend><?cs var:html_escape(Lang.Legend.GnupgKeyImport) ?> </legend>
	<?cs call:form_header_upload("gnupg_key_upload") ?>

		<input type="hidden" name="gnupg_subset" value="<?cs
			if:Data.Action == 'gnupg_public' ?>public<?cs
			else ?>secret<?cs /if ?>" />

		<ul>
			<li><?cs var:html_escape(Lang.Misc.GnupgImportKey) ?>
				<ul><li><input type="file" name="gnupg_key_file" size="50"
					maxlength="250" /></li>
				</ul>
			</li>

			<li>
				<input type="hidden" name="action" value="gnupg_do" />
				<button type="submit" name="send" value="do"><?cs
					var:html_escape(Lang.Buttons.GnupgImportKey) ?></button>
			</li>
		</ul>
	
	</form>

</fieldset>

