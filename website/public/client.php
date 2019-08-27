<?php
$PYTHON_PATH = 'venv/bin/python'; # Linux: 'venv/bin/python'
$SERVER_DIRECTORY = '../server';
$SERVER_FILE = 'server.py';

if (!empty($input = file_get_contents('php://input')))
{
	// try to launch the application
	$cmd = "$PYTHON_PATH $SERVER_FILE";
	$descriptorspec = array(
		0 => array('pipe', 'r'),
		1 => array('pipe', 'w'),
		2 => array('pipe', 'w'),
	);
	$cwd = dirname(__FILE__) . "/$SERVER_DIRECTORY";
	$process = proc_open($cmd, $descriptorspec, $pipes, $cwd);
	
	if (is_resource($process))
	{
		fwrite($pipes[0], $input);
		fclose($pipes[0]);
		
		$json = stream_get_contents($pipes[1]);
		fclose($pipes[1]);
		fclose($pipes[2]);
		proc_close($process);
	}
	else
	{
		$data = array(
			'error' => 'Failed to reach server',
			'status' => 'error',
		);
		$json = json_encode($data);
	}
}
else
{
	$data = array(
		'error' => 'No input',
		'status' => 'error',
	);
	$json = json_encode($data);
}

// Return JSON and exit
header('Content-Type: application/json');
echo $json;
