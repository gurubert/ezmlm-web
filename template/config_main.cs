<div class="title">
	<h1><?cs var:html_escape(Lang.Title.ConfigMain) ?></h1>
</div>

<div class="introduction">
	<p><?cs var:html_escape(Lang.Introduction.ConfigMain) ?></p>
</div>

<fieldset class="form">
	<legend><?cs var:html_escape(Lang.Legend.ConfigMain) ?> </legend>

	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
		<input type="hidden" name="config_subset" value="main" />

		<ul>

			<!-- public subscription and archive -->
			<li><?cs call:checkbox("p") ?></li>

			<!-- process mailman-style requests -->
			<li><?cs call:checkbox("q") ?></li>

			<!-- remove ezmlm-warn -->
			<li><?cs call:checkbox("w") ?></li>

			<!-- list owner address -->
			<li><?cs call:setting("5") ?></li>

			<!-- set main list name -->
			<li><?cs call:setting("0") ?></li>

			<!-- mysql database -->
			<?cs if:Data.Modules.mySQL ?>
				<li><?cs call:setting("6") ?></li><?cs /if ?>

			<!-- ezmlm-web administators -->
			<?cs if:Data.List.WebUsers ?>
				<li><?cs var:html_escape(Lang.Misc.AllowedToEdit) ?>: 
					<ul><li><input type="text"
					name="webusers" value="<?cs var:html_escape(Data.List.WebUsers)
					?>" size="40" /><br/>
					</li></ul></li><?cs /if ?>

			<li><!-- include default form values -->
			<?cs include:TemplateDir + '/form_common.cs' ?>

			<input type="hidden" name="action" value="config_do" />
			<button type="submit" name="send" value="do"><?cs var:html_escape(Lang.Buttons.UpdateConfiguration) ?></button></li>
		</ul>

	</form>

</fieldset>
