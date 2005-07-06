<div id="nav">

<ul>
    <li><a href="<?cs var:ScriptName ?>?action=select_list"
    <?cs if:((Data.Action == "list_create_ask")  || (Data.Action == "list_create_do") || (Data.Action == "select_list") || (Date.Action == "list_delete_ask") || (Data.Action == "list_delete_do") || (Data.Action == "list_delete_select" ) || (!Data.Action)) ?>
    	class="active">All lists</a>
	<ul id="subnav">
	    <li><a <?cs if:((!Data.Action) || (Data.Action == "select_list")) ?> class="active"<?cs /if ?>
		href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=select_list"> Select</a></li>
	    <li><a <?cs if:((Data.Action == "list_create_do" ) || (Data.Action == "list_create_ask")) ?>class="active"<?cs /if ?>
		href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_create_ask">Create</a></li>
	    <li><a <?cs if:((Data.Action == "list_delete_do" ) || (Data.Action == "list_delete_ask") || (Data.Action == "list_delete_select")) ?>class="active"<?cs /if ?>
		href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_delete_select">Delete</a></li>
	</ul>
    <?cs else ?>
        >All lists</a>
    <?cs /if ?> 
    </li>

  <?cs if:Data.List.Name ?>

    <!-- subscribers -->
    <li>
	<a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers"
	<?cs if:(Data.Action == "list_subscribers") ?>
	    class="active">Subscribers</a>
	    <ul id="subnav">
		<li><a <?cs if:(!Data.List.PartType) ?>class="active"<?cs /if ?>
		    href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers">Recipients</a></li>
		<li><a <?cs if:(Data.List.PartType == "allow") ?>class="active"<?cs /if ?>
		    href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=allow">Allow</a></li>
		<li><a <?cs if:(Data.List.PartType == "deny") ?>class="active"<?cs /if ?>
		    href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=deny">Deny</a></li>
		<li><a <?cs if:(Data.List.PartType == "mod") ?>class="active"<?cs /if ?>
		    href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=mod">Moderators</a></li>
		<li><a <?cs if:(Data.List.PartType == "digest") ?>class="active"<?cs /if ?>
		    href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=digest">Digest</a></li>
	    </ul>
	<?cs else ?>
	    >Subscribers</a>
	<?cs /if ?>
    </li>

    <!-- list config -->
    <li>
	<a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_config_ask"
	<?cs if:((Data.Action == "list_config_ask") || (Data.Action == "list_config_do")) ?>
	    class="active">Configuration</a>
	    <ul id="subnav">
	    <li><a <?cs if:((Data.Action == "list_config_do" ) || (Data.Action == "list_config_ask") || (Data.Action == "list_config_basic_ask")) ?>class="active"<?cs /if ?>
		href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_config">Basic</a></li>
	    <li><a <?cs if:((Data.Action == "list_config_do" ) || (Data.Action == "list_config_expert_ask")) ?>class="active"<?cs /if ?>
		href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_config_expert">Expert</a></li>
	    </ul></li>
	  <?cs else ?>
		>Configuration</a>
	  <?cs /if ?>
    </li>


    <!-- text files -->
    <li>
	<a href="<?cs var:ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_textfiles"
    <?cs if:((Data.Action == "list_textfiles") || (Data.Action == "edit_text_ask") || (Data.Action == "edit_text_do")) ?>
    	    class="active">Textfiles</a>
	<?cs else ?>
	    >Textfiles</a>
	<?cs /if ?>
    </li>

  <?cs /if ?>

</ul>

</div>
