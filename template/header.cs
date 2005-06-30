<!DOCTYPE html
	PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
	<title><?cs var:PageTitle ?></title>
	<meta http-equiv="pragma" content="no-cache" />	<!-- for browsers -->
	<meta http-equiv="cache-control" content="no-cache" />	<!-- for proxys -->
	<meta http-equiv="content-language" content="<?cs var:Language ?>" />
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="Author" content="guy-ezmlm[at]rucus.ru.ac.za" />
	<meta http-equiv="expire" content="-1d" />
	<link rel="stylesheet" type="text/css" href="<?cs var:Stylesheet ?>" />
</head>

<body>

<p>
<center><table border="3" align="center" cellpadding="5"><tr><td bgcolor="#e0e0ff"><font size=+3 color=#000080><strong>E Z Mailing List Manager</strong></font></td></tr></table></center>
</p>

<table border="0" cellpadding="5" cellspacing="5" align="center" width="99%"><tr><td bgcolor="#e0e0ff">



<div id="nav"><p><span>
	<a <?cs if:((Data.Action == "list_create_ask")  || (Data.Action == "list_create_do") || (Data.Action == "select_list") || (Date.Action == "list_delete_ask") || (Data.Action == "list_delete_do") || (Data.Action == "list_delete_select" ) || (!Data.Action)) ?>class="active"<?cs /if ?> 
	href="<?cs var:Data.ScriptName ?>?action=select_list">All lists</a>

	<?cs if:Data.List.Name ?>
		<a <?cs if:((Data.Action == "list_config_ask") || (Data.Action == "list_config_do")) ?>class="active"<?cs /if ?>
		href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_config_ask">Configuration</a>
		<a <?cs if:(Data.Action == "list_subscribers") ?>class="active"<?cs /if ?>
		href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers">Subscribers</a>
		<a <?cs if:((Data.Action == "list_textfiles") || (Data.Action == "edit_text_ask") || (Data.Action == "edit_text_do")) ?>class="active"<?cs /if ?>
		href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_textfiles">Textfiles</a>
	<?cs /if ?>
	
</span></p></div>

<?cs if:((Data.Action == "select_list") || (Data.Action == "list_create_ask") || (Data.Action == "list_create_do") || (Data.Action == "list_delete_ask") || (Data.Action == "list_delete_do" ) || (Data.Action == "list_delete_select" ) || (!Data.Action)) ?>
<div id="subnav"><p><span>
	<a <?cs if:((!Data.Action) || (Data.Action == "select_list")) ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=select_list">Select</a> |
	<a <?cs if:((Data.Action == "list_create_do" ) || (Data.Action == "list_create_ask")) ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_create_ask">Create</a> |
	<a <?cs if:((Data.Action == "list_delete_do" ) || (Data.Action == "list_delete_ask") || (Data.Action == "list_delete_select")) ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_delete_select">Delete</a>
</span></p></div>
<?cs /if ?>

<?cs if:(Data.Action == "list_subscribers") ?>
<div id="subnav"><p><span>
	<a <?cs if:(!Data.List.PartType) ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers">Recipients</a> |
	<a <?cs if:(Data.List.PartType == "allow") ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=allow">Allow</a> |
	<a <?cs if:(Data.List.PartType == "deny") ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=deny">Deny</a> |
	<a <?cs if:(Data.List.PartType == "mod") ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=mod">Moderators</a> |
	<a <?cs if:(Data.List.PartType == "digest") ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_subscribers&part=digest">Digest</a>
</span></p></div>
<?cs /if ?>

<?cs if:((Data.Action == "list_config_ask") || (Data.Action == "list_config_do") || (Data.Action == "edit_text_do")) ?>
<div id="subnav"><p><span>
	<a <?cs if:((Data.Action == "list_config_do" ) || (Data.Action == "list_config_ask") || (Data.Action == "list_config_basic_ask")) ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_config">Basic</a> |
	<a <?cs if:((Data.Action == "list_config_do" ) || (Data.Action == "list_config_expert_ask")) ?>class="active"<?cs /if ?>
	href="<?cs var:Data.ScriptName ?>?list=<?cs var:Data.List.Name ?>&action=list_config_expert">Expert</a>
</span></p></div>
<?cs /if ?>

