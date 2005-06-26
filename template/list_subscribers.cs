<div id="edit" class="container">

    <div class="title">

        <h2><?cs var:Lang.Misc.SubscribersTo ?> <i><?cs var:Data.List.Name ?></i></h2>
        <h3><?cs var:Data.List.Address ?></h3>
	<hr>
    </div>

    <?cs if:Data.isModerated ?>
		<!-- show warnings for wrong moderation paths -->
		<?cs include:TemplateDir + "modpath_info.cs" ?>
    <?cs /if ?>


    <div class="list">
	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	    <input type="hidden" name="state" value="edit">
	    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>">
	    <?cs if:Data.List.PartType ?>
		    <input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>">
	    <?cs /if ?>

	    <!-- scrollbox for list's subscribers -->
	    <!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
	    <?cs if:(Data.List.SubscribersCount > 25) ?>
		<?cs set:Data.ScrollSize = 25 ?>
	      <?cs else ?>
		<?cs set:Data.ScrollSize = Data.List.SubscribersCount ?>
	    <?cs /if ?>
	    <!-- TODO: this div should float to left - the buttons should be at the right -->
	    <select name="delsubscriber" tabindex="1" size="<?cs var:Data.ScrollSize ?>" multiple="yes">
		<?cs each:item = Data.List.Subscribers ?>
		    <option><?cs var:item ?></option>
		<?cs /each ?>
	    </select>
	
	    <div class="add_remove">
		<?cs if:(Data.List.SubscribersCount > 0) ?> 
		    <p><?cs var:Data.List.SubscribersCount ?> <?cs var:Lang.Misc.Subscribers ?></p>
		    <span class="button"><input type="submit" name="action" tabindex="2"
			value="<?cs var:Lang.Buttons.DeleteAddress ?>"></span>
		<?cs /if ?>
		<!-- TODO: das helper icon ist erst in der naechsten Zeile -->
		<p class="formfield"><input type="text" name="addsubscriber"
			tabindex="3" size="40"/><?cs call:help_icon("AddAddress") ?></p>
		<!-- TODO: eventuell ein BR einfuegen -->
		<?cs if:Data.Permissions.FileUpload ?>
		    <p class="formfield"><input type="file" name="addfile" size="20"
			maxlength="100" tabindex="4"/><?cs call:help_icon("AddAddressFile") ?></p>
		<?cs /if ?>
		<p class="button"><input type="submit" tabindex="5" name="action"
		      value="<?cs var:Lang.Buttons.AddAddress ?>"/></p>
	    </div>

	    <?cs if:Data.List.PartType ?>
		    <span class="button"><input type="submit" tabindex="11" name="action"
			value="<?cs var:Lang.Buttons.Configuration ?>"/>
			<?cs call:help_icon("Config") ?></span>
	    <?cs else ?>
		<div class="options">
		    <?cs if:Data.ConfigAvail.Extras ?>
		    <!-- at least one extra config option is available -->
			<h3><?cs var:Lang.Misc.AdditionalParts ?>:</h3>
		    <?cs /if ?>
		    <p>
		    <?cs if:Data.ConfigAvail.Moderation ?>
		    <!-- moderation -->
			<span class="button"><input type="submit" tabindex="6" name="action"
			    value="<?cs var:Lang.Buttons.Moderators ?>"/>
			    <?cs call:help_icon("Moderator") ?></span>
		    <?cs /if ?>

		    <?cs if:Data.ConfigAvail.DenyList ?>
		    <!-- deny lists -->
			<span class="button"><input type="submit" tabindex="7" name="action"
			    value="<?cs var:Lang.Buttons.DenyList ?>"/>
			    <?cs call:help_icon("Deny") ?></span>
		    <?cs /if ?>

		    <?cs if:Data.ConfigAvail.AllowList ?>
		    <!-- allow lists -->
			<span class="button"><input type="submit" tabindex="8" name="action"
			    value="<?cs var:Lang.Buttons.AllowList ?>"/>
			    <?cs call:help_icon("Allow") ?></span>
		    <?cs /if ?>

		    <?cs if:Data.ConfigAvail.Digest ?>
		    <!-- digest subscribers -->
			<span class="button"><input type="submit" tabindex="9" name="action"
			    value="<?cs var:Lang.Buttons.DigestSubscribers ?>"/>
			    <?cs call:help_icon("Digest") ?></span>
		    <?cs /if ?>
		    </p>

		    <p>
		    <!-- web archive -->
		    <?cs if:Data.ConfigAvail.WebArch ?>
			<span class="button"><input type="submit" tabindex="10" name="action"
			    value="<?cs var:Lang.Buttons.WebArchive ?>"/>
			    <?cs call:help_icon("WebArch") ?></span>
		    <?cs /if ?>

		    <!-- extra config options -->
		    <span class="button"><input type="submit" tabindex="11" name="action"
			value="<?cs var:Lang.Buttons.Configuration ?>"/>
			<?cs call:help_icon("Config") ?></span>

		    <span class="button"><input type="submit" tabindex="12" name="action"
			value="<?cs var:Lang.Buttons.SelectList ?>"/>
			<?cs call:help_icon("SelectList") ?></span>
		    </p>
		
		</div>
		<!-- end of list options block -->
	    <?cs /if ?>

	</form>

    </div>

</div>
