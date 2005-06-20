<div id="parts" class="container">
    <div class="title">
	<!-- TODO: einheitliche Formatierung fuer listaddress - span und css -->
	<h2><?cs var:Lang.Misc.For <i><?cs var:Data.ListName ?></i></h2>
	<h3><?cs var:Data.ListAddress ?></h3>
	<hr>
    </div>

    <!-- Moderation -->
    <?cs if:Data.isModerated ?>
	    <?cs include:TemplateDir + "modpath_info.cs" ?>
    <?cs /if ?>

    <!-- form -->
    <form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	<input type="hidden" name="state" value="<?cs var:Data.Form.State ?>">
	<input type="hidden" name="list" value="<?cs var:Data.ListName ?>">
	    <div class="list">
		

	# TODO: the same as of "display_list.cs"
	# list of moderators/administrators
	<?cs if:Data.ListCount >0 ?>
	    <!-- Keep selection box a resonable size - suggested by Sebastian Andersson -->
	    <?cs if:(Data.ListCount > 25) ?>
		<?cs set:Data.ScrollSize = 25 ?>
	      <?cs else ?>
	 	<?cs set:Data.ScrollSize = Data.ListCount ?>
	    <?cs /if ?>
	    <select name="delsubscriber" tabindex="1" multiple="true" size="<?cs var:Data.ScrollSize ?>">
		<?cs each:item = Data.List ?>
		    <!-- TODO: pretty names sind notwendig -->
		    <option><?cs var:item ?></option>
		<?cs /each ?>
	    </select>
	<?cs /if ?>


	<div class="add_remove">

	  <?cs if:Data.ListCount > 0) ?>
	    <span class="button"><input type="submit"
		value="<?cs var:Lang.Buttons.DeleteAddress ?>" name="action"/></span>
	  <?cs /if ?>

	  <span class="formfield">
	    <input type="text" name="addsubscriber" size="40"/> <?cs call:help_icon("AddAddress") ?></span>
	  <?cs if:FileUploadAllowed ?><span class="formfield">
	    <input type="filefield" name="addfile" size="20" maxlength="100"/> <?cs call:help_icon("AddAddressFile") ?></span><?cs /if ?>
	  <span class="button">
	    <input type="submit" name="action" value="<?cs var:Lang.Buttons.AddAddress ?>"/></span>
	  <span class="button">
	    <input type="submit" name="action" value="<?cs var:Lang.Buttons.Subscribers ?>"/></span>

	</div>

    </form>
</div>
