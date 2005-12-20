<div id="config" class="container">

    <div class="title">
		<h1><?cs var:Lang.Title.ConfigPosting ?></h1>
    </div>

  <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="config_subset" value="posting" />

    <div class="input"><ul>

		<li><?cs call:checkbox("u") ?></li>
		<li><?cs call:checkbox("m") ?></li>
		<li><?cs call:checkbox("o") ?></li>
		<li><?cs call:checkbox("k") ?></li>
		<li><?cs call:setting("7") ?></li>

		<!-- include default form values -->
		<?cs include:TemplateDir + '/form_common.cs' ?>

	<button type="submit" name="action" value="config_do"><?cs var:Lang.Buttons.UpdateConfiguration ?></button>
    </ul></div>

  </form>

</div>
