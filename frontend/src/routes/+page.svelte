<script lang="ts">

import HalfHourTimeInput from "$lib/components/HalfHourTimeInput.svelte";
</script>

<h1>And They Were Roommates</h1>
<!-- TODO: In future, submitting details will require authentication -->
<p>Enter your details below to get started. These details will be used to match you with a compatible roommate.</p>
<form>
    <h2>Basic Information</h2>
    <label>
        Name:
        <input type="text" name="name" required />
    </label>
    <br>

    <label>
        Student ID:
        <input type="text" name="student-id" required />
    </label>
    <br>

    <label>
        Gender:
        <select name="gender" required>
            <option value="" disabled selected>Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="non-binary">Non-binary</option>
            <option value="prefer-not-to-say">Prefer not to say</option>
        </select>
    </label>


    <h2>Timings</h2>
    <!-- In future, a lot of these pairs could be combined into a double range slider -->

    <label>
        I am likely to only work between
        <HalfHourTimeInput name="work-start" />
        and
        <HalfHourTimeInput name="work-end" />
    </label>
    <br>

    <label>
        On a night out I would go to bed at
        <HalfHourTimeInput name="night-out-bedtime" />
    </label>
    <br>

    <label>
        On a quiet weekday I would go to bed at
        <HalfHourTimeInput name="quiet-weekday-bedtime" />
    </label>
    <br>

    <label>
        On a normal weekday I would go to bed at
        <HalfHourTimeInput name="normal-weekday-bedtime" />
    </label>
    <br>

    <label>
        I would
        <select name="overnight-guests" required>
            <option value="" disabled selected>(mind having)</option>
            <option value="yes">be fine with</option>
            <option value="rather-no">rather avoid</option>
            <option value="no">not want</option>
        </select>
        people staying overnight
    </label>
    <br>

    <h2>Personality</h2>

    <label>
        I consider myself to be an
        <select name="introvert-extrovert" required>
            <option value="" disabled selected>(introvert/extrovert)</option>
            <option value="introvert">introvert</option>
            <option value="ambivert">ambivert</option>
            <option value="extrovert">extrovert</option>
            <option value="not-sure">not sure</option>
        </select>
    </label>
    <br>

    <label>
        I consider myself to be
        <select name="tidiness" required>
            <option value="" disabled selected>(tidy/messy)</option>
            <option value="5">very tidy</option>
            <option value="4">somewhat tidy</option>
            <option value="3">neither tidy nor messy</option>
            <option value="2">somewhat messy</option>
            <option value="1">very messy</option>
        </select>
    </label>
    <br>

    <label>
        I
        <select name="care-about-tidiness" required>
            <option value="" disabled selected>(care about/don't care about)</option>
            <option value="5">care a lot about</option>
            <option value="4">care somewhat about</option>
            <option value="3">neither care nor don't care about</option>
            <option value="2">don't care much about</option>
            <option value="1">don't care at all about</option>
        </select>
        my roommate's tidiness
    </label>
    <br>

    <!-- In future, these multi-text inputs could be tag-style inputs -->
    <label>
        I watch the following sports: (separate with commas)
        <input type="text" name="sports-watched" placeholder="e.g. football, basketball" />
    </label>
    <br>

    <label>
        I play the following sports: (separate with commas)
        <input type="text" name="sports-played" placeholder="e.g. tennis, swimming" />
    </label>
    <br>

    <label>
        I like the following music genres: (separate with commas)
        <input type="text" name="music-genres" placeholder="e.g. rock, classical" />
    </label>
    <br>

    <label>
        I like the following music artists: (separate with commas)
        <input type="text" name="music-artists" placeholder="e.g. The Beatles, Beyoncé" />
    </label>
    <br>

    <button type="submit">Submit</button>
</form>
