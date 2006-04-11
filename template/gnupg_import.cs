<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.GnupgKeyImport) ?> </legend>
	<!-- this form has to be "multipart/form-data" to make file upload work -->
	<form method="post" action="<?cs call:link("","","","","","") ?>"
		enctype="multipart/form-data">

		<input type="hidden" name="gnupg_subset" value="<?cs
			if:Data.Action == 'gnupg_public' ?>public<?cs
			else ?>secret<?cs /if ?>" />

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

				<input type="hidden" name="action" value="gnupg_do" />
				<button type="submit" name="send" value="do"><?cs
					var:html_escape(Lang.Buttons.GnupgImportKey) ?></button>
			</li>
		</ul>
	
	</form>

</fieldset>


