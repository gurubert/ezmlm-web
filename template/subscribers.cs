<div class="subscribers">

    <div class="title">

        <h2><?cs var:Lang.Misc.SubscribersTo ?> <i><?cs var:Data.List.Name ?></i></h2>
        <h3><?cs var:Data.List.Address ?></h3>
	<hr/>
    </div>

    <?cs if:(Data.List.hasPostMod || Data.List.hasSubMod || Data.List.hasRemoteAdmin) ?>
		<!-- show warnings for wrong moderation paths -->
		<?cs include:TemplateDir + "modpath_info.cs" ?>
    <?cs /if ?>


    <div class="list">
	<form method="post" action="<?cs var:ScriptName ?>" enctype="application/x-www-form-urlencoded">
	    <input type="hidden" name="list" value="<?cs var:Data.List.Name ?>" />
	    <?cs if:Data.List.PartType ?>
		    <input type="hidden" name="part" value="<?cs var:Data.List.PartType ?>" />
	    <?cs /if ?>

	    <!-- scrollbox for list's subscribers -->
	    <!-- Keep selection box a reasonable size - suggested by Sebastian Andersson -->
	    <?cs if:(Data.List.SubscribersCount > 25) ?>
		<?cs set:Data.ScrollSize = 25 ?>
	      <?cs else ?>
		<?cs set:Data.ScrollSize = Data.List.SubscribersCount ?>
	    <?cs /if ?>
	    <!-- TODO: this div should float to left - the buttons should be at the right -->
	    <select name="mailaddress_del" tabindex="1" size="<?cs var:Data.ScrollSize ?>" multiple="multiple">
		<?cs each:item = Data.List.Subscribers ?>
		    <option><?cs var:item ?></option>
		<?cs /each ?>
	    </select>
	
	    <div class="add_remove">
		<?cs if:(Data.List.SubscribersCount > 0) ?> 
		    <p><?cs var:Data.List.SubscribersCount ?> <?cs var:Lang.Misc.Subscribers ?></p>
		    <button type="submit" name="action" tabindex="2" value="address_del"><?cs var:Lang.Buttons.DeleteAddress ?></button>
		<?cs /if ?>
		<!-- TODO: das helper icon ist erst in der naechsten Zeile -->
		<p class="formfield"><input type="text" name="mailaddress_add"
			<?cs call:help_title("AddAddress") ?>
			tabindex="3" size="40" /><?cs call:help_icon("AddAddress") ?></p>
		<!-- TODO: eventuell ein BR einfuegen -->
		<?cs if:Data.Permissions.FileUpload ?>
		    <p class="formfield"><input type="file" name="mailaddressfile" size="20"
			<?cs call:help_title("AddAddressFile") ?>
			maxlength="100" tabindex="4" /><?cs call:help_icon("AddAddressFile") ?></p>
		<?cs /if ?>
		<button type="submit" tabindex="5" name="action" value="address_add"><?cs var:Lang.Buttons.AddAddress ?></button>
	    </div>

	    <?cs if:Data.List.PartType ?>
		<button type="submit" tabindex="11" name="action"
		    <?cs call:help_title("Config") ?> value="list_config_ask">
		    <?cs var:Lang.Buttons.Configuration ?></button><?cs call:help_icon("Config") ?>
	    <?cs else ?>
		<div class="options">
		    <!-- at least one extra config option is available -->
			<h3><?cs var:Lang.Misc.AdditionalParts ?>:</h3>
		    <p>
		    <?cs if:(Data.List.hasPostMod || Data.List.hasSubMod || Data.List.has.RemoteAdmin) ?>
		    <!-- moderation -->
			<button type="submit" tabindex="6" name="action"
			    <?cs call:help_title("Moderator") ?> value="part_mod">
			    <?cs var:Lang.Buttons.Moderators ?></button><?cs call:help_icon("Moderator") ?>
		    <?cs /if ?>

		    <?cs if:Data.List.hasDenyList ?>
		    <!-- deny lists -->
			<button type="submit" tabindex="7" name="action"
			    <?cs call:help_title("DenyList") ?> value="part_deny">
			    <?cs var:Lang.Buttons.DenyList ?></button><?cs call:help_icon("Deny") ?>
		    <?cs /if ?>

		    <?cs if:Data.list.hasAllowList ?>
		    <!-- allow lists -->
			<button type="submit" tabindex="8" name="action"
			    <?cs call:help_title("Allow") ?> value="part_allow">
			    <?cs var:Lang.Buttons.AllowList ?></button><?cs call:help_icon("Allow") ?>
		    <?cs /if ?>

		    <?cs if:Data.List.hasDigestList ?>
		    <!-- digest subscribers -->
			<button type="submit" tabindex="9" name="action"
			    <?cs call:help_title("Digest") ?> value="part_digest">
			    <?cs var:Lang.Buttons.DigestSubscribers ?></button><?cs call:help_icon("Digest") ?>
		    <?cs /if ?>
		    </p>

		    <p>
		    <!-- web archive -->
		    <?cs if:Data.List.hasWebArchive ?>
			<button type="submit" tabindex="10" name="action"
			    <?cs call:help_title("WebArchive") ?> value="web_archive">
			    <?cs var:Lang.Buttons.WebArchive ?></button><?cs call:help_icon("WebArchive") ?>
		    <?cs /if ?>

		    <!-- extra config options -->
		    <button type="submit" tabindex="11" name="action"
		        <?cs call:help_title("Config") ?> value="list_config_ask">
			<?cs var:Lang.Buttons.Configuration ?></button><?cs call:help_icon("Config") ?>

		    <button type="submit" tabindex="12" name="action"
		        <?cs call:help_title("SelectList") ?> value="select_list">
			<?cs var:Lang.Buttons.SelectList ?></button><?cs call:help_icon("SelectList") ?>
		    </p>
		
		</div>
		<!-- end of list options block -->
	    <?cs /if ?>

	</form>

    </div>

</div>
