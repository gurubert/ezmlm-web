<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgKeyImport) ?> </legend>
	<form method="post" action="<?cs call:link("","","","","","") ?>"
		enctype="application/x-www-form-urlencoded">

		<input type="hidden" name="gnupg_subset" value="public" />

		<?cs call:show_options(UI.Options.Keymanagement.Public) ?>

		<td><form method="post" action="<?cs call:link("","","","","","") ?>"
			enctype="multipart/form-data">
		<!-- this form has to be "multipart/form-data" to make file upload work -->
		<input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />

		<ul>
			<li><?cs var:html_escape(Lang.Misc.GnupgImportKey) ?>
				<ul><li><input type="file" name="gnupg_key_file" size="50"
					maxlength="250" /></li>
				</ul>
			</li>

			<li>
				<!-- include default form values -->
				<?cs include:TemplateDir + '/form_common.cs' ?>

				<input type="hidden" name="action" value="gnupg_import_key" />
				<button type="submit" name="send" value="do"><?cs
					var:html_escape(Lang.Buttons.GnupgImportKey) ?></button>
			</li>
		</ul>
	
	</form>

</fieldset>


