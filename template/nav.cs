<!-- $Id$ -->

<div id="nav_bar">
<ul>
	<?cs if:(subcount(Data.Lists) > 0) ?>
		<li><a <?cs if:(Data.Action == "list_select") ?> class="nav_active"<?cs /if ?>
			href="<?cs var:ScriptName ?>?action=list_select"
			title="<?cs var:Lang.Menue.ListSelect ?>"><?cs var:Lang.Menue.ListSelect ?></a>
		</li>
		<?cs /if ?>
	<?cs if:Data.Permissions.Create ?>
		<li><a <?cs if:(Data.Action == "list_create") ?> class="nav_active"<?cs /if ?>
			href="<?cs var:ScriptName ?>?action=list_create_ask"
			title="<?cs var:Lang.Menue.Create ?>"><?cs var:Lang.Menue.Create ?></a>
		</li>
		<?cs /if ?>


<?cs if:Data.List.Name ?>

	<li><font class="no_link"><?cs var:Lang.Menue.Properties ?> <?cs var:Data.List.Name ?></font><ul>
		<li><a <?cs if:((Data.Action == "subscribers") && ((Data.List.PartType == "") || !Data.List.PartType)) ?>class="nav_active"<?cs /if ?>
			href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers" title="<?cs var:Lang.Menue.Subscribers ?>"><?cs var:Lang.Menue.Subscribers ?></a>
			<ul>
				<li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "allow")) ?>class="nav_active"<?cs /if ?>
					href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=allow"><?cs var:Lang.Menue.AllowList ?></a></li>
				<li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "deny")) ?> class="nav_active"<?cs /if ?>
					href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=deny"><?cs var:Lang.Menue.DenyList ?></a></li>
				<li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "digest")) ?> class="nav_active"<?cs /if ?>
					href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=digest"><?cs var:Lang.Menue.DigestList ?></a></li>
				<li><a <?cs if:((Data.Action == "subscribers") &&
						(Data.List.PartType == "mod")) ?> class="nav_active"<?cs /if ?>
					href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=subscribers&part=mod"><?cs var:Lang.Menue.ModList ?></a></li>
			</ul>
		</li>

		<li><a <?cs if:(Data.Action == "config_main") ?> class="nav_active"<?cs /if ?>
			href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=main" title="<?cs var:Lang.Menue.ConfigMain ?>"><?cs var:Lang.Menue.ConfigMain ?></a>
		<ul>
			<li><a <?cs if:(Data.Action == "config_subscription") ?> class="nav_active"<?cs /if ?>
				href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=subscription" title="<?cs var:Lang.Menue.ConfigSub ?>"><?cs var:Lang.Menue.ConfigSub ?></a></li>
			<li><a <?cs if:(Data.Action == "config_posting") ?> class="nav_active"<?cs /if ?>
				href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=posting" title="<?cs var:Lang.Menue.ConfigPost ?>"><?cs var:Lang.Menue.ConfigPost ?></a></li>
			<li><a <?cs if:(Data.Action == "config_filter") ?> class="nav_active"<?cs /if ?>
				href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=filter" title="<?cs var:Lang.Menue.ConfigFilter ?>"><?cs var:Lang.Menue.ConfigFilter ?></a></li>
			<li><a <?cs if:(Data.Action == "config_archive") ?> class="nav_active"<?cs /if ?>
				href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=archive" title="<?cs var:Lang.Menue.ConfigArchive ?>"><?cs var:Lang.Menue.ConfigArchive ?></a></li>
			<li><a <?cs if:(Data.Action == "config_admin") ?> class="nav_active"<?cs /if ?>
				href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=config_ask&config_subset=admin" title="<?cs var:Lang.Menue.ConfigAdmin ?>"><?cs var:Lang.Menue.ConfigAdmin ?></a></li>
		</ul></li>

		<li><a <?cs if:((Data.Action == "textfiles") || (Data.Action == "textfile_edit")) ?> class="nav_active"<?cs /if ?>
			href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=textfiles" title="<?cs var:Lang.Menue.TextFiles ?>"><?cs var:Lang.Menue.TextFiles ?></a></li>

		<li><a <?cs if:(Data.Action == "list_delete") ?> class="nav_active"<?cs /if ?>
			href="<?cs var:ScriptName ?>?list=<?cs var:url_escape(Data.List.Name) ?>&action=list_delete_ask" title="<?cs var:Lang.Menue.Delete ?>"><?cs var:Lang.Menue.Delete ?></a></li>
		
	</ul></li>

<?cs /if ?>

	<li><a href="http://www.ezmlm.org/ezman/index.html#toc1" target="_blank" title="<?cs var:Lang.Misc.HelpLink ?>"><?cs var:Lang.Menue.Help ?></a></li>

</ul>

<!-- end of navbar div -->
</div>

